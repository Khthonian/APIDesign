import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Documentation from "./pages/Documentation";
import HomePage from "./pages/HomePage";

function Navbar() {
  return (
    <nav style={{ display: "flex", gap: "10px" }}>
      <Link to="/">Home</Link>
      <Link to="/docs">Documentations</Link>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/docs" element={<Documentation />} />
      </Routes>
    </Router>
  );
}

export default App;
