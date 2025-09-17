# Neurolytix\backend\forecasting\deep_hybrid.py

import logging
from typing import Optional

import numpy as np
import pandas as pd
from prophet import Prophet
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential

logger = logging.getLogger(__name__)

class DeepHybridForecaster:
    """
    Prophet + LSTM(residual) hybrid forecaster.
    - Prophet captures trend/seasonality/holidays.
    - LSTM models remaining autocorrelation in residuals.
    """

    def __init__(
        self,
        lstm_sequence_length: int = 30,
        lstm_epochs: int = 50,
        lstm_batch_size: int = 32,
        prophet_daily: bool = True,
        prophet_weekly: bool = True,
        prophet_yearly: bool = True,
        prophet_changepoint_prior_scale: float = 0.05,
        random_state: int = 42,
    ):
        self.sequence_length = lstm_sequence_length
        self.epochs = lstm_epochs
        self.batch_size = lstm_batch_size
        self.scaler = MinMaxScaler(feature_range=(0, 1))

        # Models
        self.prophet: Optional[Prophet] = None
        self.lstm: Optional[Sequential] = None

        # Prophet configuration
        self.prophet_daily = prophet_daily
        self.prophet_weekly = prophet_weekly
        self.prophet_yearly = prophet_yearly
        self.prophet_changepoint_prior_scale = prophet_changepoint_prior_scale
        self.random_state = random_state

        # Fitted artifacts
        self._residual_std: Optional[float] = None
        self._fitted = False

    @staticmethod
    def _make_sequences(arr: np.ndarray, seq_len: int):
        X, y = [], []
        for i in range(len(arr) - seq_len):
            X.append(arr[i : i + seq_len])
            y.append(arr[i + seq_len])
        X = np.asarray(X)
        y = np.asarray(y)
        return X.reshape((X.shape[0], X.shape[1], 1)), y

    def _build_lstm(self, timesteps: int):
        model = Sequential()
        model.add(LSTM(64, activation="tanh", input_shape=(timesteps, 1)))
        model.add(Dense(1))
        model.compile(optimizer="adam", loss="mse")
        return model

    def fit(self, df: pd.DataFrame, target_column: str):
        """
        df: must contain columns ['ds', target_column] with ds as datetime-like
        """
        logger.info("DeepHybridForecaster: Fitting…")

        work = df.copy()
        work = work[["ds", target_column]].dropna()
        work["ds"] = pd.to_datetime(work["ds"], errors="coerce")
        work.dropna(subset=["ds"], inplace=True)
        work = work.sort_values("ds")

        # ---- Prophet fit
        pdf = work.rename(columns={target_column: "y"})
        self.prophet = Prophet(
            daily_seasonality=self.prophet_daily,
            weekly_seasonality=self.prophet_weekly,
            yearly_seasonality=self.prophet_yearly,
            changepoint_prior_scale=self.prophet_changepoint_prior_scale,
        )
        self.prophet.fit(pdf)

        # In-sample Prophet prediction for residuals
        in_sample = self.prophet.predict(pdf[["ds"]])
        yhat_in = in_sample["yhat"].values
        y_true = pdf["y"].values
        residuals = y_true - yhat_in

        # Track residual dispersion for intervals
        self._residual_std = float(np.nanstd(residuals))

        # ---- LSTM on residuals
        res = residuals.reshape(-1, 1).astype(np.float32)
        res_scaled = self.scaler.fit_transform(res)
        if len(res_scaled) <= self.sequence_length + 1:
            # Not enough data; create a degenerate LSTM that predicts 0 residuals
            logger.warning(
                "Insufficient history for LSTM residuals. "
                "Will fall back to Prophet-only with zero residuals."
            )
            self.lstm = None
        else:
            X, y = self._make_sequences(res_scaled, self.sequence_length)
            self.lstm = self._build_lstm(self.sequence_length)
            early = EarlyStopping(monitor="loss", patience=5, restore_best_weights=True)
            self.lstm.fit(
                X,
                y,
                epochs=self.epochs,
                batch_size=self.batch_size,
                callbacks=[early],
                verbose=0,
            )

        self._fitted = True
        logger.info("DeepHybridForecaster: Fit completed.")

    def predict(self, df: pd.DataFrame, target_column: str, horizon: int = 30) -> pd.DataFrame:
        if not self._fitted:
            raise RuntimeError("Model not fitted. Call fit() first.")

        work = df.copy()
        work = work[["ds", target_column]].dropna()
        work["ds"] = pd.to_datetime(work["ds"], errors="coerce")
        work.dropna(subset=["ds"], inplace=True)
        work = work.sort_values("ds")

        # Prophet future forecast
        future = self.prophet.make_future_dataframe(periods=horizon, include_history=True)
        pfc = self.prophet.predict(future)
        tail = pfc.tail(horizon)[["ds", "yhat", "yhat_lower", "yhat_upper"]].reset_index(drop=True)

        # Prepare residual seed (last sequence of residuals on history)
        history_pdf = work.rename(columns={target_column: "y"})
        in_sample = self.prophet.predict(history_pdf[["ds"]])
        residuals_hist = (history_pdf["y"].values - in_sample["yhat"].values).astype(np.float32)

        # Default residual path = zeros if no LSTM or too-short history
        residual_forecast = np.zeros(horizon, dtype=np.float32)

        if self.lstm is not None and len(residuals_hist) >= self.sequence_length:
            seed = residuals_hist[-self.sequence_length :].reshape(-1, 1)
            seed_scaled = self.scaler.transform(seed)

            seq = seed_scaled.reshape(1, self.sequence_length, 1)
            preds_scaled = []
            for _ in range(horizon):
                nxt = self.lstm.predict(seq, verbose=0)
                preds_scaled.append(nxt[0, 0])
                # Roll window
                seq = np.append(seq[:, 1:, :], nxt.reshape(1, 1, 1), axis=1)

            residual_forecast = self.scaler.inverse_transform(
                np.array(preds_scaled).reshape(-1, 1)
            ).flatten()

        # Combine prophet yhat + residual LSTM
        yhat = tail["yhat"].values + residual_forecast

        # Simple PI: combine Prophet intervals with residual std (1.96 * sigma)
        # This assumes independence; it’s a pragmatic approximation.
        res_margin = 1.96 * (self._residual_std or 0.0)
        yhat_lower = tail["yhat_lower"].values - res_margin
        yhat_upper = tail["yhat_upper"].values + res_margin

        out = pd.DataFrame(
            {
                "ds": tail["ds"].values,
                "yhat": yhat,
                "yhat_lower": yhat_lower,
                "yhat_upper": yhat_upper,
            }
        )
        return out
