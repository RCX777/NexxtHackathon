import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import './App.css';
import Header from '../../components/header/Header'; 
import Feature from '../../components/feature/Feature';
import Details from '../../components/details/Details';
import PaySection from '../../components/pay-section/PaySection';

function App() {
  const location = useLocation();
  const inputValue = location.state?.inputURL || '';

  const [responseData, setResponseData] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const isTransactionTrust = false;
  const footerDescription = "If the password has not been received via SMS, please call the Raiffeisen Bank Romania Call Center at +40 21 3063002 or the phone numbers listed on the back of your card.";

  useEffect(() => {
    if (inputValue) {
      fetch(`hal/${inputValue}`)
        .then(response => response.json())
        .then(data => {
          setResponseData(data);
          setIsLoaded(true);
        })
        .catch(error => {
          console.error('Error fetching data:', error);
          setIsLoaded(true);
        });
    }
  }, [inputValue]);

  return (
    <div className="App">
      <div className="main-container">
        <Header />
        <Feature isTrust={isTransactionTrust} isLoaded={isLoaded} response={responseData} />
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
