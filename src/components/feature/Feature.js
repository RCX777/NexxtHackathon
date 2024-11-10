import React, { useState } from 'react';
import './Feature.css';

import CheckIcon from '../../assets/check.png';
import AlertIcon from '../../assets/alert.png';
import WarningIcon from '../../assets/warning.png';
import Loading from '../loading/Loading';

const notTrustReasons = [
  "Reason 1",
  "Reason 2",
  "Reason 3"
];

function Feature({ isTrust, isLoaded }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const icon = isTrust ? CheckIcon : AlertIcon;

  const toggleReasonsList = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className="feature">
      <div className="message">
        {!isLoaded && <Loading />}
        {isLoaded && <img src={icon} alt="Status icon" className="check-icon" />}
        <p>
          { !isLoaded
          ? 'Verifying ...'
          : isTrust
            ? 'Beneficiarul a fost verificat. Puteți finaliza plata cu încredere.'
            : 'Atenție! Este posibil ca această tranzacție să nu fie de încredere.'}
        </p>
      </div>
      
      {!isTrust && isLoaded && (
        <div className="reasons-toggle">
          <button onClick={toggleReasonsList} className="toggle-button">
            {isExpanded ? 'Ascunde detalii' : 'Afișează detalii'}
          </button>
          
          {isExpanded && (
            <div>
            <div className="reasons-list">
              <ul>
                {notTrustReasons.map((reason, index) => (
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
