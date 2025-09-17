import React, { useState } from "react";
import { BASE_URL } from "../services/api";

const Forecast = () => {
  const [data, setData] = useState(null);

  const fetchForecast = async () => {
    try {
      const response = await fetch(`${BASE_URL}/forecast/your-endpoint`);
      const result = await response.json();
      setData(result);
    } catch (err) {
      console.error("Error fetching forecast:", err);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-blue-700">📈 Forecast Analysis</h1>
      <button
        className="btn btn-primary mt-4"
        onClick={fetchForecast}
      >
        Load Forecast
      </button>
      {data && <pre className="mt-4">{JSON.stringify(data, null, 2)}</pre>}
    </div>
  );
};

export default Forecast;
