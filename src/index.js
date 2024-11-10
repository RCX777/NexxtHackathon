import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/home-page/HomePage';
import ReportPage from './pages/report-page/ReportPage';
import App from './pages/payment-page/App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} /> 
        <Route path="/payment" element={<App />} /> 
        <Route path="/report" element={<ReportPage />} />
      </Routes>
    </Router>
  </React.StrictMode>
);

// Performance measuring
reportWebVitals();
