import React from 'react';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
  const navigate = useNavigate();

  const handleButtonClick = (pageURL) => {
    navigate(pageURL);
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        background: '#282c34',
        color: 'white',
        textAlign: 'center',
        fontFamily: 'Arial, sans-serif'
      }}
    >
      <Typography variant="h3" component="h1" gutterBottom>
        Welcome to our Autonomous Vehicle Simulation Platform
      </Typography>
      <Typography variant="body1" gutterBottom>
        Your journey to safer and more efficient autonomous vehicles starts here.
      </Typography>
      <Box
        sx={{
          '& > :not(style)': { m: 1 },
        }}
      >
        <Button variant="contained" color="primary" onClick={() => handleButtonClick("/register")}>
          Register
        </Button>
        <Button variant="contained" color="primary" onClick={() => handleButtonClick("/login")}>
          Login
        </Button>
      </Box>
    </Box>
  );
}

export default HomePage;
