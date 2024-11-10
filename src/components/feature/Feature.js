import React, { useState, useEffect } from 'react';
import './Feature.css';

import CheckIcon from '../../assets/check.png';
import AlertIcon from '../../assets/alert.png';
import WarningIcon from '../../assets/warning.png';
import Loading from '../loading/Loading';

function Feature({ isLoaded, response }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isTrust, setIsTrust] = useState(false); // Managing trust state based on score
  const [reasons, setReasons] = useState([]);

  const icon = isTrust ? CheckIcon : AlertIcon;

  const toggleReasonsList = () => {
    setIsExpanded(!isExpanded);
  };

  // Effect to update the reasons and trust status when response is available
  useEffect(() => {
    if (response) {
      // Extracting score and top reasons from response
      const score = parseFloat(response.score);  // Ensure score is a number
      const topReasons = response['top reasons'] || [];

      // Set trust status based on score
      setIsTrust(score > 0.2); // If score > 0.2, set isTrust to true

      // Set reasons if they exist
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
      
      {/* Display reasons only if the trust is false and data is loaded */}
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
                  For more details, access <a href="/report" className="details-link">here</a>.
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
