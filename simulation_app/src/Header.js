import React from 'react';

const headerStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#007BFF',
    color: 'white',
    padding: '10px 50px',
    boxShadow: '0px 3px 6px #00000029'
};

const logoStyle = {
    fontWeight: 'bold',
    fontSize: '24px',
};

const navStyle = {
    listStyle: 'none',
    display: 'flex',
    gap: '20px'
};

function Header() {
    return (
        <header style={headerStyle}>
            <h1 style={logoStyle}>App Logo</h1>
            <nav>
                <ul style={navStyle}>
                    <li>Home</li>
                    <li>About</li>
                    <li>Contact</li>
                </ul>
            </nav>
        </header>
    );
}

export default Header;