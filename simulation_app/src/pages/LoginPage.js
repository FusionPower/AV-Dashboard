import React, { useState } from 'react';
import { useMutation, gql } from '@apollo/client';
import { Container, TextField, Button, Typography } from '@mui/material';
import { styled } from '@mui/system';


const QUERY_USER = gql`
  type Mutation {
    loginUser(username: String!, password: String!): String!
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


function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  
  const handleSubmit = event => {
    event.preventDefault();

    // submit the registration data (username, email, password)
  };
  return (
    <StyledContainer>
      <Typography variant="h4" component="h1">Login</Typography>
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
          Login
        </StyledButton>
      </StyledForm>
    </StyledContainer>

  );
}

export default LoginPage;
