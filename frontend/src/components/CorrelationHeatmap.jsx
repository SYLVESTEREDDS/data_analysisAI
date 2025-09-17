import React from "react";

const CorrelationHeatmap = ({ dataset }) => {
  if (!dataset || !dataset.preview || dataset.preview.length === 0) {
    return (
      <div className="p-4 bg-gray-100 rounded-xl text-gray-600">
        ⚡ Upload a dataset to see correlation heatmap.
      </div>
    );
  }

  // Compute correlations
  const numericCols = Object.keys(dataset.preview[0]).filter(
    (col) => !isNaN(dataset.preview[0][col])
  );

  const correlationMatrix = numericCols.map((col1) =>
    numericCols.map((col2) => {
      const x = dataset.preview.map((row) => Number(row[col1]));
      const y = dataset.preview.map((row) => Number(row[col2]));
      const n = x.length;
      const meanX = x.reduce((a, b) => a + b, 0) / n;
      const meanY = y.reduce((a, b) => a + b, 0) / n;
      const numerator = x.reduce((sum, xi, idx) => sum + (xi - meanX) * (y[idx] - meanY), 0);
      const denominator = Math.sqrt(
        x.reduce((sum, xi) => sum + (xi - meanX) ** 2, 0) *
        y.reduce((sum, yi) => sum + (yi - meanY) ** 2, 0)
      );
      return denominator === 0 ? 0 : +(numerator / denominator).toFixed(2);
    })
  );

  return (
    <div className="mt-6 p-4 bg-white shadow rounded-xl border overflow-x-auto">
      <h2 className="text-lg font-semibold mb-3">🧮 Correlation Heatmap</h2>
      <table className="border-collapse border border-gray-300 text-sm">
        <thead>
          <tr>
            <th className="border border-gray-300 p-2"> </th>
            {numericCols.map((col, idx) => (
              <th key={idx} className="border border-gray-300 p-2">{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {correlationMatrix.map((row, i) => (
            <tr key={i}>
              <td className="border border-gray-300 p-2 font-semibold">{numericCols[i]}</td>
              {row.map((val, j) => (
                <td
                  key={j}
                  className="border border-gray-300 p-2 text-center"
                  style={{
                    backgroundColor: `rgba(79, 70, 229, ${Math.abs(val)})`,
                    color: val > 0.5 || val < -0.5 ? "white" : "black",
                  }}
                >
                  {val}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <p className="mt-2 text-gray-600 text-sm">
        Values range from -1 (strong negative correlation) to 1 (strong positive correlation)
      </p>
    </div>
  );
};

export default CorrelationHeatmap;
