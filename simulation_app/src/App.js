import { ApolloProvider } from '@apollo/client';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import client from './apollo';

import Header from './Header';
import Footer from './Footer';
import HomePage from "./pages/HomePage";
import RegistrationPage from "./pages/RegistrationPage";
import LoginPage from "./pages/LoginPage";
import "./App.css";
import UserContext from "./UserContext"
import { useState } from "react";


function App() {
  const [user, setUser] = useState(null);

  return (
    <UserContext.Provider value={{user, setUser}}>
      <ApolloProvider client={client}>
        <Router>
          <div className="App">
            <Header />
            <Routes>
              <Route path="/register" element={<RegistrationPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/" element={<HomePage />} />
            </Routes>
            <Footer />
          </div>
        </Router>
      </ApolloProvider>
    </UserContext.Provider>
  );
}

export default App;
