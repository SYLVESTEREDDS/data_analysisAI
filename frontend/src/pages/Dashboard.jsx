// src/pages/Dashboard.jsx
import React, { useState } from "react";
import UploadDataset from "../components/UploadDataset";
import DatasetTable from "../components/DatasetTable";
import DatasetVisualizer from "../components/DatasetVisualizer";
import ForecastForm from "../components/ForecastForm";
import ClusterScatter from "../components/ClusterScatter";

const Dashboard = () => {
  const [dataset, setDataset] = useState(null);

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <h1 className="text-3xl font-bold mb-2 text-gray-800">📊 Neurolytix Dashboard</h1>
      <p className="text-gray-600">
        Welcome to Neurolytix — your AI-powered data analytics platform.  
        Upload datasets, explore insights, visualize data, run forecasts, clustering, and anomaly detection.
      </p>

      {/* Upload, Table, Visualization, Forecast, and Clustering */}
      <div className="space-y-6">
        <UploadDataset onUploadSuccess={setDataset} />
        <DatasetTable dataset={dataset} />
        <DatasetVisualizer dataset={dataset} />
        <ForecastForm dataset={dataset} />
        <ClusterScatter dataset={dataset} />
      </div>
    </div>
  );
};

export default Dashboard;
