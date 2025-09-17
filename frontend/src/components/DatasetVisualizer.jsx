import React, { useState } from "react";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  ScatterChart,
  Scatter,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const chartTypes = ["Line", "Bar", "Scatter", "Area"];

const DatasetVisualizer = ({ dataset }) => {
  const [xKey, setXKey] = useState("");
  const [yKey, setYKey] = useState("");
  const [chartType, setChartType] = useState("Line");

  if (!dataset || !dataset.preview || dataset.preview.length === 0) {
    return (
      <div className="p-4 bg-gray-100 rounded-xl text-gray-600">
        📉 No dataset available. Upload a dataset to visualize.
      </div>
    );
  }

  const columns = Object.keys(dataset.preview[0]);

  const renderChart = () => {
    const commonProps = { data: dataset.preview };

    switch (chartType) {
      case "Line":
        return (
          <LineChart {...commonProps}>
            <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
            <XAxis dataKey={xKey} />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey={yKey} stroke="#4f46e5" />
          </LineChart>
        );
      case "Bar":
        return (
          <BarChart {...commonProps}>
            <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
            <XAxis dataKey={xKey} />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey={yKey} fill="#4f46e5" />
          </BarChart>
        );
      case "Scatter":
        return (
          <ScatterChart {...commonProps}>
            <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
            <XAxis dataKey={xKey} />
            <YAxis />
            <Tooltip />
            <Legend />
            <Scatter dataKey={yKey} fill="#4f46e5" />
          </ScatterChart>
        );
      case "Area":
        return (
          <AreaChart {...commonProps}>
            <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
            <XAxis dataKey={xKey} />
            <YAxis />
            <Tooltip />
            <Legend />
            <Area type="monotone" dataKey={yKey} stroke="#4f46e5" fill="#c7d2fe" />
          </AreaChart>
        );
      default:
        return null;
    }
  };

  return (
    <div className="mt-6 p-4 bg-white shadow rounded-xl border">
      <h2 className="text-lg font-semibold mb-3">📊 Dataset Visualization</h2>

      <div className="grid grid-cols-3 gap-4 mb-4">
        <div>
          <label className="block text-sm font-medium">X-Axis</label>
          <select
            className="mt-1 p-2 border rounded-lg w-full"
            value={xKey}
            onChange={(e) => setXKey(e.target.value)}
          >
            <option value="">-- Select column --</option>
            {columns.map((col, idx) => (
              <option key={idx} value={col}>
                {col}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium">Y-Axis</label>
          <select
            className="mt-1 p-2 border rounded-lg w-full"
            value={yKey}
            onChange={(e) => setYKey(e.target.value)}
          >
            <option value="">-- Select column --</option>
            {columns.map((col, idx) => (
              <option key={idx} value={col}>
                {col}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium">Chart Type</label>
          <select
            className="mt-1 p-2 border rounded-lg w-full"
            value={chartType}
            onChange={(e) => setChartType(e.target.value)}
          >
            {chartTypes.map((type, idx) => (
              <option key={idx} value={type}>
                {type}
              </option>
            ))}
          </select>
        </div>
      </div>

      {xKey && yKey ? (
        <ResponsiveContainer width="100%" height={300}>
          {renderChart()}
        </ResponsiveContainer>
      ) : (
        <div className="p-3 text-gray-600 bg-gray-50 rounded-lg">
          ⚡ Select X and Y axes to visualize data.
        </div>
      )}
    </div>
  );
};

export default DatasetVisualizer;
