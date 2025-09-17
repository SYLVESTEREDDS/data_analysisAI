import pandas as pd
from models.forecast_model import Forecast
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet


class ForecastService:
    def __init__(self):
        self.model_handler = Forecast()

    def make_forecast(self, df: pd.DataFrame, column: str, periods: int = 10) -> pd.DataFrame:
        """
        Run forecasting pipeline for a given dataframe and column.

        Args:
            df (pd.DataFrame): Input dataset
            column (str): Column to forecast
            periods (int): Number of future periods

        Returns:
            pd.DataFrame: Forecasted values
        """
        # Ensure time index exists
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index("date")
        else:
            df.index = pd.date_range(start="2020-01-01", periods=len(df), freq="D")

        # Clean dataset
        series = df[column].dropna()

        try:
            # Try Prophet
            forecast = self._forecast_with_prophet(series, periods)
        except Exception:
            try:
                # Fallback: ARIMA
                forecast = self._forecast_with_arima(series, periods)
            except Exception:
                # Final fallback: Moving Average
                forecast = self._forecast_with_moving_average(series, periods)

        return forecast

    def _forecast_with_prophet(self, series: pd.Series, periods: int) -> pd.DataFrame:
        df = pd.DataFrame({"ds": series.index, "y": series.values})
        model = Prophet(daily_seasonality=True, yearly_seasonality=True)
        model.fit(df)

        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)

        return forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periods)

    def _forecast_with_arima(self, series: pd.Series, periods: int) -> pd.DataFrame:
        model = ARIMA(series, order=(5, 1, 0))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=periods)

        forecast_df = pd.DataFrame({
            "ds": pd.date_range(start=series.index[-1] + pd.Timedelta(days=1), periods=periods, freq="D"),
            "yhat": forecast
        })
        return forecast_df

    def _forecast_with_moving_average(self, series: pd.Series, periods: int) -> pd.DataFrame:
        last_value = series.iloc[-1]
        forecast = [last_value] * periods
        forecast_df = pd.DataFrame({
            "ds": pd.date_range(start=series.index[-1] + pd.Timedelta(days=1), periods=periods, freq="D"),
            "yhat": forecast
        })
        return forecast_df
