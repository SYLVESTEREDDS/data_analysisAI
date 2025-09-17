import React, { useEffect, useState } from "react";
import axios from "../utils/axiosConfig";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from "recharts";

const ForecastChart = ({ datasetId, actualColumn }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const res = await axios.get("/visualization/forecast_visualization", {
        params: { dataset_id: datasetId, actual_column: actualColumn }
      });

      const chartData = res.data.dates.map((date, idx) => {
        const item = { date, actual: res.data.actual[idx] };
        Object.keys(res.data.forecasts).forEach(model => {
          item[model] = res.data.forecasts[model][idx];
        });
        return item;
      });
      setData(chartData);
    };
    fetchData();
  }, [datasetId, actualColumn]);

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="actual" stroke="#000000" strokeWidth={2} dot={{ r: 2 }} />
        {data[0] && Object.keys(data[0]).filter(key => key !== "date" && key !== "actual").map((model, idx) => (
          <Line key={model} type="monotone" dataKey={model} stroke={["#ff0000","#00cc00","#0000ff"][idx % 3]} dot={false} />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
};

export default ForecastChart;
