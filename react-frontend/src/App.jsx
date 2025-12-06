import React from 'react';
import { BrowserRouter as Router, Routes,Route } from 'react-router-dom';
import Home from './pages/Home';
import Transactions from './pages/Transactions';
import Reports from './pages/Reports';
import Layout from "./Layout.jsx";
import {TransactionsProvider} from "./components/TransactionsContext.jsx";
import Budgets from "./pages/Budgets.jsx";

function App() {
  return (
    <Router>
      <div>
          <TransactionsProvider>
            <Routes>
                <Route path="/" element={<Layout><Home /></Layout>} />
                <Route path="/transactions" element={<Layout><Transactions /></Layout>} />
                <Route path="/budgets" element={<Layout><Budgets /></Layout>} />
                <Route path="/reports" element={<Layout><Reports /></Layout>} />
            </Routes>
          </TransactionsProvider>
      </div>
    </Router>
  );
}

export default App;