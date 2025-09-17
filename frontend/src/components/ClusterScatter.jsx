import React, { useState } from "react";
import axios from "axios";
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

const ClusterScatter = ({ dataset }) => {
  const [xKey, setXKey] = useState("");
  const [yKey, setYKey] = useState("");
  const [nClusters, setNClusters] = useState(3);
  const [method, setMethod] = useState("kmeans");
  const [clusters, setClusters] = useState([]);
  const [loading, setLoading] = useState(false);

  if (!dataset) {
    return (
      <div className="p-4 bg-gray-100 rounded-xl text-gray-600">
        ⚡ Upload a dataset to enable clustering visualization.
      </div>
    );
  }

  const columns = Object.keys(dataset.preview[0]);

  const handleCluster = async () => {
    if (!xKey || !yKey) return;

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", dataset.file);
      formData.append("n_clusters", nClusters);
      formData.append("method", method);

      const res = await axios.post("http://localhost:8000/api/cluster/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setClusters(res.data.clusters);
    } catch (error) {
      console.error("Clustering error:", error);
    } finally {
      setLoading(false);
    }
  };

  const colors = ["#4f46e5", "#f59e0b", "#10b981", "#ef4444", "#8b5cf6"];

  return (
    <div className="mt-6 p-4 bg-white shadow rounded-xl border">
      <h2 className="text-lg font-semibold mb-3">🌌 Cluster Scatter Plot</h2>

      <div className="grid grid-cols-4 gap-4 mb-4">
        <div>
          <label className="block text-sm font-medium">X-Axis</label>
          <select className="mt-1 p-2 border rounded-lg w-full" value={xKey} onChange={(e) => setXKey(e.target.value)}>
            <option value="">-- Select column --</option>
            {columns.map((col, idx) => (<option key={idx} value={col}>{col}</option>))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium">Y-Axis</label>
          <select className="mt-1 p-2 border rounded-lg w-full" value={yKey} onChange={(e) => setYKey(e.target.value)}>
            <option value="">-- Select column --</option>
            {columns.map((col, idx) => (<option key={idx} value={col}>{col}</option>))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium">Clusters</label>
          <input type="number" min="1" max="10" value={nClusters} onChange={(e) => setNClusters(e.target.value)} className="mt-1 p-2 border rounded-lg w-full" />
        </div>

        <div>
          <label className="block text-sm font-medium">Method</label>
          <select value={method} onChange={(e) => setMethod(e.target.value)} className="mt-1 p-2 border rounded-lg w-full">
            <option value="kmeans">KMeans</option>
            <option value="agglomerative">Agglomerative</option>
          </select>
        </div>
      </div>

      <button onClick={handleCluster} disabled={loading} className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
        {loading ? "Clustering..." : "Generate Clusters"}
      </button>

      {clusters.length > 0 && xKey && yKey && (
        <ResponsiveContainer width="100%" height={300} className="mt-4">
          <ScatterChart>
            <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
            <XAxis type="number" dataKey={xKey} />
            <YAxis type="number" dataKey={yKey} />
            <Tooltip cursor={{ strokeDasharray: '3 3' }} />
            <Legend />
            {clusters.map((cluster, idx) => (
              <Scatter key={idx} name={`Cluster ${idx + 1}`} data={cluster.map(row => ({ [xKey]: Number(row[xKey]), [yKey]: Number(row[yKey]) }))} fill={colors[idx % colors.length]} />
            ))}
          </ScatterChart>
        </ResponsiveContainer>
      )}
    </div>
  );
};

export default ClusterScatter;
