import React, { useEffect, useState } from "react";
import axios from "../utils/axiosConfig";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";
import MonitoringWidget from "../components/MonitoringWidget";
import ForecastChart from "../components/ForecastChart";

const AdvancedDashboard = () => {
  const [kpis, setKpis] = useState({});
  const [recentDataset, setRecentDataset] = useState([]);
  const [forecastData, setForecastData] = useState([]);
  const [forecastFileName, setForecastFileName] = useState("latest_forecast.csv");

  useEffect(() => {
    // Fetch KPIs
    const fetchKpis = async () => {
      try {
        const res = await axios.get("/dashboard/kpis");
        setKpis(res.data);
      } catch (err) {
        console.error("Failed to fetch KPIs", err);
      }
    };

    // Fetch recent dataset trends
    const fetchRecentDataset = async () => {
      try {
        const res = await axios.get("/dashboard/recent_dataset_trends");
        setRecentDataset(res.data);
      } catch (err) {
        console.error("Failed to fetch recent dataset", err);
      }
    };

    // Fetch recent forecast data
    const fetchForecastData = async () => {
      try {
        const res = await axios.get("/dashboard/recent_forecasts");
        setForecastData(res.data);
      } catch (err) {
        console.error("Failed to fetch forecast data", err);
      }
    };

    fetchKpis();
    fetchRecentDataset();
    fetchForecastData();
  }, []);

  // Download Handlers
  const handleDownloadCSV = async (fileName) => {
    try {
      const res = await axios.get(`/reports/download_forecast_csv?forecast_file=${fileName}`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", fileName);
      document.body.appendChild(link);
      link.click();
    } catch (err) {
      console.error("Failed to download CSV", err);
    }
  };

  const handleDownloadPDF = async (fileName) => {
    try {
      const res = await axios.get(`/reports/generate_forecast_pdf?forecast_file=${fileName}`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", fileName.replace(".csv", ".pdf"));
      document.body.appendChild(link);
      link.click();
    } catch (err) {
      console.error("Failed to download PDF", err);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Neurolytix Advanced Dashboard</h1>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="p-4 bg-blue-600 text-white rounded shadow">
          <h2 className="text-xl">Total Datasets</h2>
          <p className="text-2xl font-bold">{kpis.total_datasets || 0}</p>
        </div>
        <div className="p-4 bg-green-600 text-white rounded shadow">
          <h2 className="text-xl">Datasets Uploaded Today</h2>
          <p className="text-2xl font-bold">{kpis.uploaded_today || 0}</p>
        </div>
        <div className="p-4 bg-purple-600 text-white rounded shadow">
          <h2 className="text-xl">Total Forecasts</h2>
          <p className="text-2xl font-bold">{kpis.total_forecasts || 0}</p>
        </div>
        <div className="p-4 bg-orange-600 text-white rounded shadow">
          <h2 className="text-xl">Top Trend Column</h2>
          <p className="text-2xl font-bold">{kpis.top_trend_column || "-"}</p>
        </div>
      </div>

      {/* Recent Dataset Trends Chart */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-2">Recent Dataset Trends</h2>
        {recentDataset.length > 0 && (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={recentDataset}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="ds" />
              <YAxis />
              <Tooltip />
              {Object.keys(recentDataset[0])
                .filter(key => key !== "ds")
                .map((col, idx) => (
                  <Line
                    key={idx}
                    type="monotone"
                    dataKey={col}
                    stroke={["#8884d8", "#82ca9d", "#ff7300", "#ff0000"][idx % 4]}
                  />
                ))}
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>

      {/* Forecast Chart */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-2">Recent Forecasts</h2>
        {forecastData.length > 0 && (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={forecastData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="ds" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="yhat" stroke="#8884d8" />
              {forecastData[0].yhat_lower && (
                <>
                  <Line type="monotone" dataKey="yhat_lower" stroke="#82ca9d" strokeDasharray="5 5" />
                  <Line type="monotone" dataKey="yhat_upper" stroke="#ff7300" strokeDasharray="5 5" />
                </>
              )}
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>

      {/* Download Buttons */}
      <div className="mb-6 flex gap-4">
        <button
          className="px-4 py-2 bg-blue-500 text-white rounded shadow hover:bg-blue-700"
          onClick={() => handleDownloadCSV(forecastFileName)}
        >
          Download Forecast CSV
        </button>
        <button
          className="px-4 py-2 bg-red-500 text-white rounded shadow hover:bg-red-700"
          onClick={() => handleDownloadPDF(forecastFileName)}
        >
          Download Forecast PDF
        </button>
      </div>

      {/* Additional Download Buttons */}
      <div className="mt-4 flex gap-4">
        <button
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-800"
          onClick={() => handleDownloadCSV("latest_forecast.csv")}
        >
          Download CSV
        </button>
        <button
          className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-800"
          onClick={() => handleDownloadPDF("latest_forecast.csv")}
        >
          Download PDF
        </button>
      </div>

      {/* Embedded Monitoring Widget */}
      <div className="mt-8">
        <MonitoringWidget />
        <ForecastChart datasetId="dataset123" actualColumn="sales" />
      </div>
    </div>
  );
};

export default AdvancedDashboard;
