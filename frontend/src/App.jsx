import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './styles/App.css'

import Navbar from './components/Navbar.jsx'
import SensorCard from './components/SensorCard.jsx'

function App() {
  const [count, setCount] = useState(0)

  return (
   <>
      <Navbar
        deviceName="Raspberry Pi 5"
        status="offline"
      />

      <main className='dashboard'>
        {/*Mock data for display test*/}
        <section className='card-grid'>
          
          <SensorCard
            title="Temperature"
            value={30}
            unit={" C"}
            min={24}
            max={33}
          />

          <SensorCard
            title="Humidity"
            value={49.9}
            unit=" %"
            min={50}
            max={80}
          />    

          <SensorCard
            title="pH"
            value={6.9}
            unit=""
            min="5.5"
            max="7.0"
          />

        </section>

      </main>
   </>
  )
}

export default App
