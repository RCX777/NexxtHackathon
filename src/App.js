import React from 'react';
import './App.css';
import Header from './components/header/Header'; 
import Feature from './components/feature/Feature';
import Details from './components/details/Details';
import PaySection from './components/pay-section/PaySection';

function App() {
  const isTransactionTrust = false;
  const footerDescription = "If the password has not been received via SMS, please call the Raiffeisen Bank Romania Call Center at +40 21 3063002 or the phone numbers listed on the back of your card.";
  return (
    <div className="App">
      <div className="main-container">
        <Header />
        <Feature isTrust={isTransactionTrust} />
        <Details />
        <PaySection />
        <footer className="footer">
          <p>{footerDescription}</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
