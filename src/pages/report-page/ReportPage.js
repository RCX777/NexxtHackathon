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
        <h1>Security of Payments</h1>
        <hr className="divider" />
        <p>
          Aceasta este o descriere simplă a raportului. Aici poți adăuga informații suplimentare despre raportul curent.
        </p>

        <section className="additional-container">
          <p>Acesta este un container suplimentar care urmează după descriere.</p>
        </section>
        <hr className="divider" />
        <section className="download-pdf">
          <img src={PDFIcon}></img>
          <h2>Download the report in PDF format:</h2>
        </section>
        <button className="download-btn">Download PDF</button>
      </section>
      </div>
    </div>
  );
}

export default ReportPage;
