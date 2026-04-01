import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './styles/App.css'

import Navbar from './components/Navbar.jsx'
import SensorCard from './components/SensorCard.jsx'
import SensorChart from './components/SensorChart.jsx'

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
            unit={" °C"}
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

        {/*SENSOR CHART*/}
        <section className="sensor-chart-grid" style={{ marginTop: "40px" }}>
          <SensorChart
            title="Temperature Chart"
            unit="°C"
            data={[21, 24, 25, 26, 28, 27, 29, 30, 28, 27]}
          />

          <SensorChart
            title="Humidity Chart"
            unit="%"
            data={[33, 55, 58, 60, 57, 62, 65, 61, 59, 63]}
          />

          <SensorChart
            title="pH Chart"
            unit=""
            data={[4.0, 6.1, 6.3, 6.5, 6.4, 6.6, 6.7, 6.5, 6.8, 6.9]}
          />
        </section>

      </main>
   </>
  )
}

export default App
