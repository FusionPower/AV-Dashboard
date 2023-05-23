import React, { useState } from 'react';
import { useMutation, gql } from '@apollo/client';
import { Container, TextField, Button, Typography } from '@mui/material';
import { styled } from '@mui/system';


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
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [createUser, { loading, error }] = useMutation(CREATE_USER);
  const handleSubmit = async (event) => {
    event.preventDefault();
    const response = await createUser({variables: {username, email, password}});
    console.log(response);
  };

  return (
    <StyledContainer>
      <Typography variant="h4" component="h1">Register</Typography>
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
      </StyledForm>
    </StyledContainer>
  );
}

export default RegistrationPage;
