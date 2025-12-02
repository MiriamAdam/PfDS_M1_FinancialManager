import React from 'react';
import { BrowserRouter as Router, Routes,Route } from 'react-router-dom';
import Home from './pages/Home';
import Transactions from './pages/Transactions';
import Reports from './pages/Reports';
import Layout from "./Layout.jsx";

function App() {
  return (
    <Router>
      <div>
        <Routes>
            <Route path="/" element={<Layout><Home /></Layout>} />
            <Route path="/transactions" element={<Layout><Transactions /></Layout>} />
            <Route path="/reports" element={<Layout><Reports /></Layout>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;