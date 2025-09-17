import React, { useEffect, useState } from "react";
import axios from "../utils/axiosConfig";

const MonitoringWidget = () => {
  const [jobs, setJobs] = useState([]);
  const [alerts, setAlerts] = useState([]);

  const fetchJobs = async () => {
    const res = await axios.get("/monitoring_dashboard/active_jobs");
    setJobs(res.data);
  };

  const fetchAlerts = async () => {
    const res = await axios.get("/monitoring_dashboard/recent_alerts");
    setAlerts(res.data);
  };

  useEffect(() => {
    fetchJobs();
    fetchAlerts();
    const interval = setInterval(() => {
      fetchJobs();
      fetchAlerts();
    }, 60000); // refresh every 60 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-4 bg-gray-100 rounded shadow">
      <h2 className="text-xl font-bold mb-2">Monitoring Dashboard</h2>

      <div className="mb-4">
        <h3 className="font-semibold">Active Jobs</h3>
        {jobs.length === 0 ? (
          <p>No active monitoring jobs</p>
        ) : (
          <ul className="list-disc list-inside">
            {jobs.map((job) => (
              <li key={job.id}>
                <strong>{job.id}</strong> | Next Run: {job.next_run_time} | Args: {JSON.stringify(job.args)}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div>
        <h3 className="font-semibold">Recent Alerts</h3>
        {alerts.length === 0 ? (
          <p>No recent alerts</p>
        ) : (
          <table className="table-auto border-collapse border border-gray-400 w-full text-sm">
            <thead>
              <tr>
                {Object.keys(alerts[0]).map((col) => (
                  <th key={col} className="border px-2 py-1">{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {alerts.map((row, idx) => (
                <tr key={idx}>
                  {Object.keys(row).map((col) => (
                    <td key={col} className="border px-2 py-1">{row[col]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default MonitoringWidget;
