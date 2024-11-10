import React, { useEffect, useState } from 'react';
import './ReportPage.css';
import Header from '../../components/header/Header';
import { useLocation } from 'react-router-dom';
import PDFIcon from '../../assets/pdf.png';

function ReportPage() {
  const location = useLocation();
  const pdfURL = location.state?.pdfURL;

  const [downloadUrl, setDownloadUrl] = useState(null);

  useEffect(() => {
    if (pdfURL) {
      setDownloadUrl(pdfURL);
    }
  }, [pdfURL]);

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

          <section className="download-pdf">
            <img src={PDFIcon} alt="PDF Icon" />
            <h2>Download the report in PDF format:</h2>
          </section>

          {downloadUrl ? (
            <a href={downloadUrl} download="report.pdf" className="download-btn">
              Download Report
            </a>
          ) : (
            <p>PDF report is not available.</p>
          )}
        </section>
      </div>
    </div>
  );
}

export default ReportPage;
