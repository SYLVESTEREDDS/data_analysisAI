import React, { useState } from "react";
import axios from "axios";

const Upload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/api/datasets/upload", formData);
      setMessage(res.data.message);
    } catch (err) {
      setMessage("Upload failed.");
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Upload Dataset</h1>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button
        className="ml-2 px-4 py-2 bg-blue-600 text-white rounded"
        onClick={handleUpload}
      >
        Upload
      </button>
      {message && <p className="mt-4">{message}</p>}
    </div>
  );
};

export default Upload;
