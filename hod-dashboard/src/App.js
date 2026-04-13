import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <Router>
      <div className="App min-h-screen bg-cyber-dark">
        <Dashboard />
      </div>
    </Router>
  );
}

export default App;