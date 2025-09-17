import React, { useState } from "react";
import axios from "../utils/axiosConfig";

const ScheduledMonitoring = () => {
  const [datasetId, setDatasetId] = useState("");
  const [targetColumn, setTargetColumn] = useState("");
  const [userEmail, setUserEmail] = useState("");
  const [message, setMessage] = useState("");

  const handleSchedule = async () => {
    try {
      const res = await axios.post("/alerts/schedule_monitoring", {
        dataset_id: datasetId,
        target_column: targetColumn,
        user_email: userEmail
      });
      setMessage(res.data.message);
    } catch (err) {
      console.error(err);
      setMessage("Failed to schedule monitoring");
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Scheduled Monitoring</h1>
      <div className="mb-2">
        <input
          placeholder="Dataset ID"
          value={datasetId}
          onChange={(e) => setDatasetId(e.target.value)}
          className="border p-2 mr-2"
        />
        <input
          placeholder="Target Column"
          value={targetColumn}
          onChange={(e) => setTargetColumn(e.target.value)}
          className="border p-2 mr-2"
        />
        <input
          placeholder="Your Email"
          value={userEmail}
          onChange={(e) => setUserEmail(e.target.value)}
          className="border p-2 mr-2"
        />
        <button className="px-4 py-2 bg-green-600 text-white rounded" onClick={handleSchedule}>
          Schedule Monitoring
        </button>
      </div>
      {message && <p className="mt-2 text-blue-600">{message}</p>}
    </div>
  );
};

export default ScheduledMonitoring;
