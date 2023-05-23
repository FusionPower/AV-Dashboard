import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MockedProvider } from '@apollo/client/testing';
import { GraphQLError } from 'graphql';
import LoginPage, { LOGIN_USER } from '../pages/LoginPage';
import { screen } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';

global.console = {
    log: jest.fn(),
    // keep other methods or you will have issues
    error: console.error,
    warn: console.warn,
    info: console.info,
    debug: console.debug,
  };

// Mocks for successful and failed login
const mocks = [
  {
    request: {
      query: LOGIN_USER,
      variables: {
        username: "test",
        password: "test123"
      },
    },
    result: {
      data: {
        loginUser: {
          ok: "Login Successful",
          user: { username: "test" }
        }
      },
    },
  },
  {
    request: {
      query: LOGIN_USER,
      variables: {
        username: "wrong",
        password: "wrong123"
      },
    },
    result: {
      errors: [new GraphQLError('Invalid credentials')],
    },
  },
];

test("renders LoginPage and checks if form works correctly", async () => {
  const { getByLabelText, getByRole } = render(
    <MockedProvider mocks={mocks} addTypename={false}>
      <Router>
        <LoginPage />
      </Router>
    </MockedProvider>
  );

  const usernameField = screen.getByLabelText(/Username/i);
  const passwordField = screen.getByLabelText(/Password/i);
  const submitButton = screen.getByRole("button", { name: /Login/i });

  // Check initial state
  expect(usernameField).toBeInTheDocument();
  expect(passwordField).toBeInTheDocument();
  expect(submitButton).toBeInTheDocument();
  expect(usernameField.value).toBe("");
  expect(passwordField.value).toBe("");

  // Update fields and check their values
  fireEvent.change(usernameField, { target: { value: "test" } });
  fireEvent.change(passwordField, { target: { value: "test123" } });

  expect(usernameField.value).toBe("test");
  expect(passwordField.value).toBe("test123");

  // Submit form and check if mutation is fired successfully
  fireEvent.click(submitButton);
  
  // Let's wait until our mocked mutation resolves and the component re-renders
  // We're expecting console.log to have been called here, since that's what you're doing on a successful login
  await waitFor(() => expect(console.log).toHaveBeenCalledTimes(1));
});

test("renders LoginPage and checks failed login", async () => {
  const { getByLabelText, getByRole } = render(
    <MockedProvider mocks={mocks} addTypename={false}>
      <Router>
        <LoginPage />
      </Router>
    </MockedProvider>
  );

  const usernameField = screen.getByLabelText(/Username/i);
  const passwordField = screen.getByLabelText(/Password/i);
  const submitButton = screen.getByRole("button", { name: /Login/i });

  // Update fields with wrong credentials
  fireEvent.change(usernameField, { target: { value: "wrong" } });
  fireEvent.change(passwordField, { target: { value: "wrong123" } });

  // Submit form
  fireEvent.click(submitButton);

  // Wait for the error to occur, again we're expecting a console.log here
  await waitFor(() => expect(console.log).toHaveBeenCalledTimes(1));
});

