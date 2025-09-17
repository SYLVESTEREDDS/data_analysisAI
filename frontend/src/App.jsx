import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import Forecasting from "./pages/Forecasting";
import Visualization from "./pages/Visualization";
import Login from "./pages/Login";
import PrivateRoute from "./components/PrivateRoute";
import { AuthProvider } from "./context/AuthContext";
import AdvancedDashboard from "./pages/AdvancedDashboard";
import Anomalies from "./pages/Anomalies";
import ForecastComparison from "./pages/ForecastComparison";
import Analytics from "./pages/Analytics";
import Forecast from "./pages/Forecast";

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50 flex">
          {/* Sidebar */}
          <aside className="w-64 bg-gray-900 text-white flex flex-col">
            <h1 className="text-2xl font-bold p-4 border-b border-gray-700">
              Neurolytix
            </h1>
            <nav className="flex-1 p-4">
              <ul className="space-y-4">
                <li>
                  <Link to="/" className="hover:text-blue-400">Dashboard</Link>
                </li>
                <li>
                  <Link to="/upload" className="hover:text-blue-400">Upload Dataset</Link>
                </li>
                <li>
                  <Link to="/forecasting" className="hover:text-blue-400">Forecasting</Link>
                </li>
                <li>
                  <Link to="/visualization" className="hover:text-blue-400">Visualization</Link>
                </li>
                <li>
                  <Link to="/advanced-dashboard" className="hover:text-blue-400">Advanced Dashboard</Link>
                </li>
                <li>
                  <Link to="/anomalies" className="hover:text-blue-400">Anomaly Detection</Link>
                </li>
                <li>
                  <Link to="/forecast-comparison" className="hover:text-blue-400">Forecast Comparison</Link>
                </li>
                <li>
                  <Link to="/analytics" className="hover:text-blue-400">Analytics</Link>
                </li>
                <li>
                  <Link to="/forecast" className="hover:text-blue-400">Forecast</Link>
                </li>
              </ul>
            </nav>
          </aside>

          {/* Main Content */}
          <main className="flex-1 p-6 bg-gray-100">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route
                path="/"
                element={
                  <PrivateRoute>
                    <Dashboard />
                  </PrivateRoute>
                }
              />
              <Route
                path="/upload"
                element={
                  <PrivateRoute>
                    <Upload />
                  </PrivateRoute>
                }
              />
              <Route
                path="/forecasting"
                element={
                  <PrivateRoute>
                    <Forecasting />
                  </PrivateRoute>
                }
              />
              <Route
                path="/visualization"
                element={
                  <PrivateRoute>
                    <Visualization />
                  </PrivateRoute>
                }
              />
              <Route
                path="/advanced-dashboard"
                element={
                  <PrivateRoute>
                    <AdvancedDashboard />
                  </PrivateRoute>
                }
              />
              <Route
                path="/anomalies"
                element={
                  <PrivateRoute>
                    <Anomalies />
                  </PrivateRoute>
                }
              />
              <Route
                path="/forecast-comparison"
                element={
                  <PrivateRoute>
                    <ForecastComparison />
                  </PrivateRoute>
                }
              />
              <Route
                path="/analytics"
                element={
                  <PrivateRoute>
                    <Analytics />
                  </PrivateRoute>
                }
              />
              <Route
                path="/forecast"
                element={
                  <PrivateRoute>
                    <Forecast />
                  </PrivateRoute>
                }
              />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
