import React from 'react';
import { Link } from 'react-router-dom';

const headerStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#007BFF',
    color: 'white',
    padding: '10px 50px',
    boxShadow: '0px 3px 6px #00000029',
};

const logoStyle = {
    fontWeight: 'bold',
    fontSize: '24px',
    cursor: 'pointer',
};

const navStyle = {
    listStyle: 'none',
    display: 'flex',
    gap: '20px',
};

const navItemStyle = {
    cursor: 'pointer',
    transition: 'color 0.3s ease',
};

function Header() {
    return (
        <header style={headerStyle}>
            <h1 style={logoStyle}>App Logo</h1>
            <nav>
                <ul style={navStyle}>
                    <li style={navItemStyle}>
                        <Link to="/" style={{ textDecoration: 'none', color: 'white' }}>Home</Link>
                    </li>
                    <li style={navItemStyle}>
                        <Link to="/about" style={{ textDecoration: 'none', color: 'white' }}>About</Link>
                    </li>
                    <li style={navItemStyle}>
                        <Link to="/contact" style={{ textDecoration: 'none', color: 'white' }}>Contact</Link>
                    </li>
                </ul>
            </nav>
        </header>
    );
}

export default Header;
