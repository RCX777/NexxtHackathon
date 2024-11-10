import React from 'react';
import './ReportPage.css';
import Header from '../../components/header/Header';

import PDFIcon from '../../assets/pdf.png';

function ReportPage() {
  return (
    <div className="ReportPage">
 
      <Header />
      <hr className="divider" />
      <div className="background-container">
      <section className="report-container">
        <h1>Payments Security</h1>
        <p>
        Reliability Analytics for websites evaluates factors like security, user reviews, and potential fraud risks to determine if a site is trustworthy for transactions.
        </p>
        <hr className="divider" />

        <section className="additional-container">
          <p>Acesta este un container suplimentar care urmează după descriere.</p>
        </section>
        <hr className="divider" />
        <section className="download-pdf">
          <img src={PDFIcon}></img>
          <h2>Download the report in PDF format:</h2>
        </section>
        <button className="download-btn">Download Report</button>
      </section>
      </div>
    </div>
  );
}

export default ReportPage;
