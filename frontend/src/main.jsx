import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles/index.css'
import App from './App.jsx'
import Navbar from './components/Navbar.jsx'
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <div>
      <Navbar
        deviceName="Raspberry Pi 5"
        status="offline"         // Set to offline to see the offline icon
        lastUpdated="10:42 AM"
      />
    </div>
  </StrictMode>,
)
