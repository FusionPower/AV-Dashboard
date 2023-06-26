import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';
import UserContext from './UserContext';
import { BrowserRouter as Router } from 'react-router-dom';

test('renders correct component', () => {
  render(
      <UserContext.Provider value={{ user: 'testuser', setUser: jest.fn() }}>
        <App />
      </UserContext.Provider>
  );

  // Use the getByText method from react-testing-library to check if the correct component has been rendered
  expect(screen.getByText('Welcome to our Autonomous Vehicle Simulation Platform')).toBeInTheDocument();
});
