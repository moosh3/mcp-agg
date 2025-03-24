import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { MantineProvider, createTheme } from '@mantine/core';
import '@mantine/core/styles.css';
import './App.css';

import {
  Login,
  Register,
  Dashboard,
  MCPUrl,
  AppsList,
  AppConfig,
  ToolsList,
  Apps
} from './pages';

import {
  AuthLayout,
  MainLayout
} from './layouts';

// Custom theme configuration
const theme = createTheme({
  primaryColor: 'blue',
  defaultRadius: 'md',
});

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  
  // Check if user is authenticated on app load
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  // Auth state handlers
  const login = (token: string) => {
    localStorage.setItem('token', token);
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  return (
    <MantineProvider theme={theme}>
      <Router>
        <Routes>
          {/* Auth Routes */}
          <Route element={<AuthLayout />}>
            <Route path="/login" element={
              isAuthenticated ? <Navigate to="/dashboard" /> : <Login onLogin={login} />
            } />
            <Route path="/register" element={
              isAuthenticated ? <Navigate to="/dashboard" /> : <Register onRegister={login} />
            } />
          </Route>
          
          {/* Protected Routes */}
          <Route element={<MainLayout onLogout={logout} isAuthenticated={isAuthenticated} />}>
            <Route path="/" element={
              isAuthenticated ? <Navigate to="/dashboard" /> : <Navigate to="/login" />
            } />
            <Route path="/dashboard" element={
              isAuthenticated ? <Dashboard /> : <Navigate to="/login" />
            } />
            <Route path="/mcp-url" element={
              isAuthenticated ? <MCPUrl /> : <Navigate to="/login" />
            } />
            <Route path="/apps" element={
              isAuthenticated ? <Apps /> : <Navigate to="/login" />
            } />
            <Route path="/apps-list" element={
              isAuthenticated ? <AppsList /> : <Navigate to="/login" />
            } />
            <Route path="/apps/:appId/config" element={
              isAuthenticated ? <AppConfig /> : <Navigate to="/login" />
            } />
            <Route path="/apps/:appId/tools" element={
              isAuthenticated ? <ToolsList /> : <Navigate to="/login" />
            } />
          </Route>
        </Routes>
      </Router>
    </MantineProvider>
  );
}

export default App;
