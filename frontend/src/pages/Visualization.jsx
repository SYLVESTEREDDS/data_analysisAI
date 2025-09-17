import React, { useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";

const Visualization = () => {
  const [datasetId, setDatasetId] = useState("");
  const [columns, setColumns] = useState("");
  const [plotData, setPlotData] = useState([]);

  const handleVisualize = async () => {
    try {
      const res = await axios.get("http://localhost:8000/api/visualization/line_plot", {
        params: { dataset_id: datasetId, columns }
      });
      setPlotData(res.data.plot_data);
    } catch (err) {
      console.error("Visualization failed", err);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Dataset Visualization</h1>

      <input
        className="border p-2 mr-2"
        placeholder="Dataset ID"
        value={datasetId}
        onChange={(e) => setDatasetId(e.target.value)}
      />
      <input
        className="border p-2 mr-2"
        placeholder="Columns (comma-separated)"
        value={columns}
        onChange={(e) => setColumns(e.target.value)}
      />
      <button
        className="px-4 py-2 bg-purple-600 text-white rounded"
        onClick={handleVisualize}
      >
        Visualize
      </button>

      {plotData.length > 0 &&
        plotData.map((colData, idx) => (
          <div key={idx} className="mt-6">
            <h2 className="font-bold mb-2">{colData.column}</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart
                data={colData.series}
                margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="x" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="y" stroke="#8884d8" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        ))}
    </div>
  );
};

export default Visualization;
