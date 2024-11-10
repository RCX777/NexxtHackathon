import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import HomePageIcon from '../../assets/homepage.png';
import './HomePage.css';

function MainPage() {
  const [inputValue, setInputValue] = useState('');
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleNavigate = () => {
    navigate('/payment', { state: { inputURL: inputValue } });
  };

  return (
    <div className="main-page">
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        placeholder="Enter text here"
        className="text-input"
      />
      <img src={HomePageIcon} alt="Homepage" />
      <button onClick={handleNavigate}>Pay</button>
    </div>
  );
}

export default MainPage;
