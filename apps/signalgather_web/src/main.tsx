import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import './index.css'

const container = document.getElementById('root')
if (!container) throw new Error('#root is missing from index.html')

createRoot(container).render(
  <StrictMode>
    {/* Mounted under /app by claude_agent's SPA route (see apps/claude_agent/app.py). */}
    <BrowserRouter basename="/app">
      <App />
    </BrowserRouter>
  </StrictMode>,
)
