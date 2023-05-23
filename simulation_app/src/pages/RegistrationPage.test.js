import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { MockedProvider } from '@apollo/client/testing';
import RegistrationPage, { CREATE_USER } from '../pages/RegistrationPage';
import { screen } from '@testing-library/react';


// Improve this console and make tests for wrong inputs
global.console = {
    log: jest.fn(),
    // keep other methods or you will have issues
    error: console.error,
    warn: console.warn,
    info: console.info,
    debug: console.debug,
  };


// Mocks for successful and failed registration
const mocks = [
  {
    request: {
      query: CREATE_USER,
      variables: {
        username: "test",
        email: "test@email.com",
        password: "test123"
      },
    },
    result: {
      data: {
        createUser: {
          ok: "User Created",
          user: { username: "test" }
        }
      },
    },
  },

];

test("renders RegistrationPage and checks if form works correctly", async () => {
  const { getByLabelText, getByRole } = render(
    <MockedProvider mocks={mocks} addTypename={false}>
      <RegistrationPage />
    </MockedProvider>
  );

  const usernameField = screen.getByLabelText(/Username/i);
  const emailField = screen.getByLabelText(/Email/i);
  const passwordField = screen.getByLabelText(/Password/i);
  const submitButton = screen.getByRole("button", { name: /Register/i });

  // Check initial state
  expect(usernameField).toBeInTheDocument();
  expect(emailField).toBeInTheDocument();
  expect(passwordField).toBeInTheDocument();
  expect(submitButton).toBeInTheDocument();
  expect(usernameField.value).toBe("");
  expect(emailField.value).toBe("");
  expect(passwordField.value).toBe("");

  // Update fields and check their values
  fireEvent.change(usernameField, { target: { value: "test" } });
  fireEvent.change(emailField, { target: { value: "test@email.com" } });
  fireEvent.change(passwordField, { target: { value: "test123" } });

  expect(usernameField.value).toBe("test");
  expect(emailField.value).toBe("test@email.com");
  expect(passwordField.value).toBe("test123");

  // Submit form and check if mutation is fired successfully
  fireEvent.click(submitButton);
  
  // Let's wait until our mocked mutation resolves and the component re-renders
  await waitFor(() => expect(console.log).toHaveBeenCalledTimes(1));
});
