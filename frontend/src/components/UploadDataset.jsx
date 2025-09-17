import React, { useState } from "react";
import api from "../utils/axiosConfig";

const UploadDataset = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("⚠️ Please select a CSV file to upload.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await api.post("/upload_dataset/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setMessage(`✅ Successfully uploaded: ${res.data.filename}`);
      if (onUploadSuccess) {
        onUploadSuccess(res.data);
      }
    } catch (error) {
      setMessage(`❌ Upload failed: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 bg-white shadow rounded-xl border">
      <h2 className="text-lg font-semibold mb-3">📂 Upload Dataset</h2>
      <input
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        className="mb-3 block w-full border border-gray-300 rounded-lg cursor-pointer text-sm"
      />
      <button
        onClick={handleUpload}
        disabled={loading}
        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
      >
        {loading ? "Uploading..." : "Upload"}
      </button>
      {message && <p className="mt-2 text-sm">{message}</p>}
    </div>
  );
};

export default UploadDataset;
