import React from 'react';

const footerStyle = {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#007BFF',
    color: 'white',
    padding: '20px 0',
    position: 'fixed',
    bottom: 0,
    width: '100%',
    boxShadow: '0px -3px 6px #00000029'
};

function Footer() {
    return (
        <footer style={footerStyle}>
            <p>© 2023 My App. All rights reserved.</p>
        </footer>
    );
}

export default Footer;
