import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.tsx';
import { BrowserRouter } from "react-router-dom";


const rootElement = document.getElementById('root');


if (rootElement) {
  // 3. Create the root once.
  const root = createRoot(rootElement);

  // 4. Render all components (StrictMode, BrowserRouter, App) wrapped together.
  root.render(
    <StrictMode>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </StrictMode>
  );
} else {
  console.error('Root element not found');
}

// The second, separate createRoot call should be removed.
