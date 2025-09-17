// frontend/src/utils/exportData.js

/**
 * Utility to export data from Neurolytix frontend
 * Supports: JSON, CSV
 */

/**
 * Export JSON data
 * @param {Object} data - The data to export
 * @param {string} filename - Filename without extension
 */
export function exportJSON(data, filename = "export") {
  const jsonStr = JSON.stringify(data, null, 2);
  const blob = new Blob([jsonStr], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = `${filename}.json`;
  link.click();

  URL.revokeObjectURL(url);
}

/**
 * Export CSV data
 * @param {Array} data - Array of objects (e.g., table rows)
 * @param {string} filename - Filename without extension
 */
export function exportCSV(data, filename = "export") {
  if (!Array.isArray(data) || data.length === 0) {
    console.error("Invalid data format for CSV export");
    return;
  }

  // Extract headers
  const headers = Object.keys(data[0]);
  const csvRows = [];

  // Add header row
  csvRows.push(headers.join(","));

  // Add data rows
  for (const row of data) {
    const values = headers.map((header) => JSON.stringify(row[header] ?? ""));
    csvRows.push(values.join(","));
  }

  const csvStr = csvRows.join("\n");
  const blob = new Blob([csvStr], { type: "text/csv" });
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = `${filename}.csv`;
  link.click();

  URL.revokeObjectURL(url);
}
