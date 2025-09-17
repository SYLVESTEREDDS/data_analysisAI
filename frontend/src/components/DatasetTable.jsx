import React from "react";

const DatasetTable = ({ dataset }) => {
  if (!dataset || !dataset.preview || dataset.preview.length === 0) {
    return (
      <div className="p-4 bg-gray-100 rounded-xl text-gray-600">
        📊 No dataset preview available. Upload a dataset to see it here.
      </div>
    );
  }

  const columns = Object.keys(dataset.preview[0]);

  return (
    <div className="mt-4 p-4 bg-white shadow rounded-xl border overflow-x-auto">
      <h2 className="text-lg font-semibold mb-3">📊 Dataset Preview</h2>
      <table className="min-w-full border border-gray-300 text-sm">
        <thead className="bg-gray-200">
          <tr>
            {columns.map((col, idx) => (
              <th key={idx} className="px-3 py-2 border border-gray-300 text-left">
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {dataset.preview.map((row, rowIndex) => (
            <tr key={rowIndex} className="hover:bg-gray-50">
              {columns.map((col, colIndex) => (
                <td key={colIndex} className="px-3 py-2 border border-gray-300">
                  {row[col]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <p className="mt-2 text-gray-600 text-sm">
        Showing first {dataset.preview.length} rows of{" "}
        <span className="font-semibold">{dataset.filename}</span>
      </p>
    </div>
  );
};

export default DatasetTable;
