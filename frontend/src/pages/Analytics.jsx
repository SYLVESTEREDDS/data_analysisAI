// frontend/src/pages/Analytics.jsx

import React, { useState } from "react";
import axios from "axios";
import { exportJSON, exportCSV } from "../utils/exportData";

const Analytics = () => {
  const [datasetId, setDatasetId] = useState("");
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchSummary = async () => {
    if (!datasetId) return;
    setLoading(true);

    try {
      const res = await axios.get(`http://127.0.0.1:8000/analytics/summary`, {
        params: { dataset_id: datasetId },
      });
      setSummary(res.data);
    } catch (err) {
      console.error("Error fetching summary:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <h1 className="text-3xl font-bold mb-4 text-indigo-600">
        📊 Analytics Dashboard
      </h1>

      {/* Dataset Input */}
      <div className="flex space-x-2">
        <input
          type="text"
          placeholder="Enter Dataset ID"
          value={datasetId}
          onChange={(e) => setDatasetId(e.target.value)}
          className="border p-2 rounded w-64"
        />
        <button
          onClick={fetchSummary}
          disabled={loading}
          className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 disabled:opacity-50"
        >
          {loading ? "Loading..." : "Get Summary"}
        </button>
      </div>

      {/* Summary Results */}
      {summary && (
        <div className="bg-white p-4 rounded shadow-md space-y-4">
          <h2 className="text-xl font-semibold text-gray-700">
            Dataset Summary
          </h2>

          <p>
            <strong>Rows:</strong> {summary.n_rows} |{" "}
            <strong>Columns:</strong> {summary.n_columns}
          </p>

          <div>
            <h3 className="font-medium text-gray-600">Columns:</h3>
            <ul className="list-disc pl-6">
              {summary.columns.map((col, idx) => (
                <li key={idx}>{col}</li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-medium text-gray-600">Missing Values:</h3>
            <pre className="bg-gray-100 p-2 rounded text-sm">
              {JSON.stringify(summary.missing_values, null, 2)}
            </pre>
          </div>

          <div>
            <h3 className="font-medium text-gray-600">Data Types:</h3>
            <pre className="bg-gray-100 p-2 rounded text-sm">
              {JSON.stringify(summary.dtypes, null, 2)}
            </pre>
          </div>

          {/* Export Options */}
          <div className="flex space-x-2 pt-4">
            <button
              onClick={() => exportJSON(summary, "dataset_summary")}
              className="bg-green-500 text-white px-3 py-2 rounded hover:bg-green-600"
            >
              Export JSON
            </button>
            <button
              onClick={() => exportCSV([summary], "dataset_summary")}
              className="bg-blue-500 text-white px-3 py-2 rounded hover:bg-blue-600"
            >
              Export CSV
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Analytics;
