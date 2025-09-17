import React from "react";
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const ChartView = ({ data, xKey, yKey, title }) => {
  if (!data || data.length === 0) {
    return (
      <div className="p-4 bg-gray-100 rounded-xl text-gray-600">
        📉 No data available for visualization.
      </div>
    );
  }

  return (
    <div className="mt-6 p-4 bg-white shadow rounded-xl border">
      <h2 className="text-lg font-semibold mb-3">{title}</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
          <XAxis dataKey={xKey} />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey={yKey}
            stroke="#4f46e5"
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ChartView;
