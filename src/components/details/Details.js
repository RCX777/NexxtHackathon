import React from 'react';
import './Details.css';
import dummyData from '../../data/dummyDetails';

function Details() {
  const data = dummyData[0];

  return (
    <div className="details">
      <h2>Enter the password</h2>
      <p>Please enter the password received via SMS in the field below to confirm the transaction.</p>

      <div className="details-item">
        <div className="label">Merchant:</div>
        <div className="value">{data.comerciant}</div>
      </div>

      <div className="details-item">
        <div className="label">Description:</div>
        <div className="value">{data.descriere}</div>
      </div>

      <div className="details-item">
        <div className="label">Amount:</div>
        <div className="value">549 RON</div>
      </div>

      <div className="details-item">
        <div className="label">Date:</div>
        <div className="value">2024.11.10</div>
      </div>

      <div className="details-item">
        <div className="label">Card number:</div>
        <div className="value">**** **** **** 1234</div>
      </div>
    </div>
  );
}

export default Details;
