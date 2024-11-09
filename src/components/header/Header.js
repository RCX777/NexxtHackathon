import React from 'react';
import './Header.css';

// Importează logo-ul din folderul assets
import logo from '../../assets/RaiffeisenBank.svg';

function Header() {
  return (
    <header className="header">
      <img src={logo} alt="Logo" className="logo left-logo" />
    </header>
  );
}

export default Header;
