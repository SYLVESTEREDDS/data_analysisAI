import React, { useState } from "react";
import axios from "axios";

const Forecasting = () => {
  const [datasetId, setDatasetId] = useState("");
  const [targetColumn, setTargetColumn] = useState("");
  const [horizon, setHorizon] = useState(30);
  const [forecast, setForecast] = useState([]);

  const handleForecast = async () => {
    try {
      const res = await axios.get("http://localhost:8000/api/forecasting/predict", {
        params: { dataset_id: datasetId, target_column: targetColumn, horizon }
      });
      setForecast(res.data.forecast);
    } catch (err) {
      console.error("Forecasting failed", err);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Forecasting</h1>

      <div className="mb-2">
        <input
          className="border p-2 mr-2"
          placeholder="Dataset ID"
          value={datasetId}
          onChange={(e) => setDatasetId(e.target.value)}
        />
        <input
          className="border p-2 mr-2"
          placeholder="Target Column"
          value={targetColumn}
          onChange={(e) => setTargetColumn(e.target.value)}
        />
        <input
          className="border p-2 mr-2 w-24"
          type="number"
          placeholder="Horizon"
          value={horizon}
          onChange={(e) => setHorizon(Number(e.target.value))}
        />
        <select
          className="border p-2 mr-2"
          value={modelType}
          onChange={(e) => setModelType(e.target.value)}
        >
          <option value="lstm">LSTM</option>
          <option value="prophet">Prophet</option>
          <option value="ensemble">Ensemble</option>
        </select>
        <button
          className="px-4 py-2 bg-green-600 text-white rounded"
          onClick={handleForecast}
        >
          Forecast
        </button>
      </div>

      {forecast.length > 0 && (
        <div className="mt-4">
          <h2 className="font-bold mb-2">Forecast Results</h2>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={forecast} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="ds" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="yhat" stroke="#8884d8" />
              {forecast[0].yhat_lower && (
                <>
                  <Line type="monotone" dataKey="yhat_lower" stroke="#82ca9d" strokeDasharray="5 5" />
                  <Line type="monotone" dataKey="yhat_upper" stroke="#ff7300" strokeDasharray="5 5" />
                </>
              )}
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
};

export default Forecasting;
