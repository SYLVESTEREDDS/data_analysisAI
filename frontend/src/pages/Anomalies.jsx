// Neurolytix/frontend/src/pages/Anomalies.jsx
import React from "react";

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
  <select
    className="border p-2 mr-2"
    value={method}
    onChange={(e) => setMethod(e.target.value)}
  >
    <option value="zscore">Z-Score</option>
    <option value="isolation_forest">Isolation Forest</option>
  </select>
  <button className="px-4 py-2 bg-red-600 text-white rounded" onClick={handleDetect}>
    Detect Anomalies
  </button>
  <button
    className="px-4 py-2 bg-blue-600 text-white rounded ml-2"
    onClick={handleSendAlert}
  >
    Send Alert
  </button>
  {/* New yellow Send Alert button */}
  <button
    className="px-4 py-2 bg-yellow-600 text-white rounded mt-2"
    onClick={handleSendAlert}
  >
    Send Alert
  </button>
</div>


const Anomalies = () => {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">🔍 Anomaly Detection</h1>
      <p className="mt-2 text-gray-600">
        Here you’ll be able to run anomaly detection on datasets.
      </p>
    </div>
  );
};

export default Anomalies;   // 👈 make sure this is here

