// Import the core React library
import React from 'react';

// Import the ReactDOM client for rendering the application
import ReactDOM from 'react-dom/client';

// Import global CSS styles
import './index.css';

// Import the main App component
import App from './App';

// Create the root element for the React application
// and attach it to the DOM element with id "root"
const root = ReactDOM.createRoot(document.getElementById('root'));   

// Render the application inside React StrictMode
// StrictMode helps identify potential problems during development
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);