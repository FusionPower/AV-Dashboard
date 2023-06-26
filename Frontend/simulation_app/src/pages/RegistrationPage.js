import React, { useState } from 'react';
import { useMutation, gql } from '@apollo/client';
import { Container, TextField, Button, Typography, Box, Link } from '@mui/material';
import { styled } from '@mui/system';
import { useNavigate } from 'react-router-dom';

export const CREATE_USER = gql`
  mutation CreateUser($username: String!, $email: String!, $password: String!) {
    createUser(username: $username, email: $email, password: $password) {
      ok
      user {
        id
        username
      }
    }
  }
`;

const StyledContainer = styled(Container)({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  height: '100vh',
  backgroundColor: '#f5f5f5',
});

const StyledForm = styled('form')({
  width: '100%',
  maxWidth: '400px',
  marginTop: '20px',
});

const StyledButton = styled(Button)({
  marginTop: '20px',
});

function RegistrationPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [createUser, { loading, error }] = useMutation(CREATE_USER);
  const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await createUser({variables: {username, email, password}});
    console.log(response);
    navigate('/login');
  };

  return (
    <StyledContainer>
      <Typography variant="h3" component="h1" gutterBottom>
        Welcome to our Simulation Platform
      </Typography>
      <Typography variant="h5" component="h2" gutterBottom>
        Create an account
      </Typography>
      <Box sx={{ mt: 2 }}>
        <Typography variant="body1">
          Start uploading and managing your autonomous vehicle simulation tests by creating an account.
        </Typography>
      </Box>
      <StyledForm onSubmit={handleSubmit}>
        <TextField
          label="Username"
          variant="outlined"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          fullWidth
          required
          margin="normal"
        />
        <TextField
          label="Email"
          variant="outlined"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          fullWidth
          required
          margin="normal"
        />
        <TextField
          label="Password"
          variant="outlined"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          type="password"
          fullWidth
          required
          margin="normal"
        />
        <StyledButton
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
        >
          Register
        </StyledButton>
        <Box sx={{ mt: 2 }}>
          <Typography variant="body1">
            Already have an account? <Link onClick={() => navigate('/login')}>Login</Link>
          </Typography>
        </Box>
      </StyledForm>
    </StyledContainer>
  );
}

export default RegistrationPage;
