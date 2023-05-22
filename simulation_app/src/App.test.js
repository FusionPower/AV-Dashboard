import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import App from './App';
import UserContext from './UserContext';

test('renders correct component', () => {
  render(
    <UserContext.Provider value={{ user: 'testuser', setUser: jest.fn() }}>
        <App />
    </UserContext.Provider>
  );

  // Use the getByText method from react-testing-library to check if the correct component has been rendered
  expect(screen.getByText('Home Page')).toBeInTheDocument();
});
