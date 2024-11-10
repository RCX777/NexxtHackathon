import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';  // Import Link
import './Feature.css';

import CheckIcon from '../../assets/check.png';
import AlertIcon from '../../assets/alert.png';
import WarningIcon from '../../assets/warning.png';
import Loading from '../loading/Loading';

function Feature({ isLoaded, response, pdfURL }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isTrust, setIsTrust] = useState(false);
  const [reasons, setReasons] = useState([]);

  const icon = isTrust ? CheckIcon : AlertIcon;

  const toggleReasonsList = () => {
    setIsExpanded(!isExpanded);
  };

  useEffect(() => {
    if (response) {
      const score = parseFloat(response.score);
      const topReasons = response['top reasons'] || [];
      setIsTrust(score > 0.2);
      setReasons(topReasons);
    }
  }, [response]);

  return (
    <div className="feature">
      <div className="message">
        {!isLoaded && <Loading />}
        {isLoaded && <img src={icon} alt="Status icon" className="check-icon" />}
        <p>
          { !isLoaded
          ? 'Verifying...'
          : isTrust
            ? 'The beneficiary has been verified. You can complete the payment with confidence.'
            : 'Attention! This transaction may not be trustworthy.'}
        </p>
      </div>
      
      {!isTrust && isLoaded && reasons.length > 0 && (
        <div className="reasons-toggle">
          <button onClick={toggleReasonsList} className="toggle-button">
            {isExpanded ? 'Hide reasons' : 'Show reasons'}
          </button>
          
          {isExpanded && (
            <div>
              <div className="reasons-list">
                <ul>
                  {reasons.map((reason, index) => (
                    <li key={index}>
                      <img src={WarningIcon} alt="Warning icon" className="list-icon" />
                      {reason}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="more-details">
                <p>
                  For more details, access <Link to="/report" state={{ pdfURL }} className="details-link">here</Link>.
                </p>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Feature;
