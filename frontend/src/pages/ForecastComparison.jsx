import React, { useState } from "react";
import axios from "../utils/axiosConfig";

const ForecastComparison = () => {
  const [datasetId, setDatasetId] = useState("");
  const [actualColumn, setActualColumn] = useState("");
  const [results, setResults] = useState(null);

  const handleCompare = async () => {
    try {
      const res = await axios.get("/forecast_evaluation/compare_forecasts", {
        params: { dataset_id: datasetId, actual_column: actualColumn }
      });
      setResults(res.data);
    } catch (err) {
      console.error(err);
      alert("Failed to compare forecasts");
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Forecast Comparison</h1>
      <div className="mb-4">
        <input
          placeholder="Dataset ID"
          value={datasetId}
          onChange={(e) => setDatasetId(e.target.value)}
          className="border p-2 mr-2"
        />
        <input
          placeholder="Actual Column"
          value={actualColumn}
          onChange={(e) => setActualColumn(e.target.value)}
          className="border p-2 mr-2"
        />
        <button className="px-4 py-2 bg-blue-600 text-white rounded" onClick={handleCompare}>
          Compare Forecasts
        </button>
      </div>

      {results && (
        <div className="mt-4">
          <h2 className="font-bold mb-2">Evaluation Metrics</h2>
          <table className="table-auto border-collapse border border-gray-400">
            <thead>
              <tr>
                <th className="border px-2 py-1">Model</th>
                <th className="border px-2 py-1">MAE</th>
                <th className="border px-2 py-1">RMSE</th>
                <th className="border px-2 py-1">MAPE (%)</th>
              </tr>
            </thead>
            <tbody>
              {Object.keys(results).map((model) => (
                <tr key={model}>
                  <td className="border px-2 py-1">{model}</td>
                  <td className="border px-2 py-1">{results[model].MAE}</td>
                  <td className="border px-2 py-1">{results[model].RMSE}</td>
                  <td className="border px-2 py-1">{results[model].MAPE}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default ForecastComparison;
