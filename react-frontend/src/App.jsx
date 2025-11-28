import React from 'react';
import { BrowserRouter as Router, Routes,Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </div>
    </Router>
  );
}

const Home = () => <h2>Home Page</h2>;

export default App;