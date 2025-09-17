import React, { useState } from "react";
import axios from "axios";
import ChartView from "./ChartView";

const ForecastForm = ({ dataset }) => {
  const [column, setColumn] = useState("");
  const [periods, setPeriods] = useState(10);
  const [forecast, setForecast] = useState(null);
  const [loading, setLoading] = useState(false);

  if (!dataset) {
    return (
      <div className="p-4 bg-gray-100 rounded-xl text-gray-600">
        ⚡ Upload a dataset first to enable forecasting.
      </div>
    );
  }

  const columns = Object.keys(dataset.preview[0]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setForecast(null);

    try {
      const formData = new FormData();
      formData.append("file", dataset.file);
      formData.append("column", column);
      formData.append("periods", periods);

      const res = await axios.post("http://localhost:8000/forecast/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setForecast(res.data.forecast);
    } catch (error) {
      console.error("Forecast error:", error);
    } finally {
      setLoading(false);
    }
  };

  // Convert forecast array into chartable format
  const forecastData = forecast
    ? forecast.map((val, idx) => ({
        period: idx + 1,
        value: val,
      }))
    : [];

  return (
    <div className="mt-6 p-4 bg-white shadow rounded-xl border">
      <h2 className="text-lg font-semibold mb-3">🔮 Forecasting</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium">Select Column</label>
          <select
            className="mt-1 p-2 border rounded-lg w-full"
            value={column}
            onChange={(e) => setColumn(e.target.value)}
            required
          >
            <option value="">-- Choose column --</option>
            {columns.map((col, idx) => (
              <option key={idx} value={col}>
                {col}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium">Forecast Periods</label>
          <input
            type="number"
            className="mt-1 p-2 border rounded-lg w-full"
            value={periods}
            min="1"
            onChange={(e) => setPeriods(e.target.value)}
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
        >
          {loading ? "Processing..." : "Generate Forecast"}
        </button>
      </form>

      {forecast && (
        <div className="mt-4">
          <h3 className="font-semibold">📈 Forecast Result:</h3>
          <ul className="list-disc pl-5 mt-2">
            {forecast.map((val, idx) => (
              <li key={idx}>
                Period {idx + 1}: <span className="font-mono">{val}</span>
              </li>
            ))}
          </ul>

          {/* Chart */}
          <ChartView
            data={forecastData}
            xKey="period"
            yKey="value"
            title="Forecast Trend"
          />
        </div>
      )}
    </div>
  );
};

export default ForecastForm;
