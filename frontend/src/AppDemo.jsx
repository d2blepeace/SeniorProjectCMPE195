import "./styles/App.css";

import Navbar from "./components/Navbar.jsx";
import SensorCard from "./components/SensorCard.jsx";
import SensorChart from "./components/SensorChart.jsx";

function AppDemo() {
    return (
        <>
        <Navbar deviceName="Raspberry Pi 5" status="online" />

        <main className="dashboard">
            <section className="card-grid">
            <SensorCard
                title="Temperature"
                value={30}
                unit=" °C"
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
            <SensorCard title="pH" value={6.9} unit="" min="5.5" max="7.0" />
            </section>

            <section className="sensor-chart-grid" style={{ marginTop: "40px" }}>
            <SensorChart
                title="Temperature Chart"
                unit="°C"
                data={[21, 24, 25, 26, 28, 27, 29]}
            />
            <SensorChart
                title="Humidity Chart"
                unit="%"
                data={[33, 55, 58, 60, 57, 62]}
            />
            <SensorChart
                title="pH Chart"
                unit=""
                data={[4.0, 6.1, 6.3, 6.5, 6.4]}
            />
            </section>
        </main>
        </>
    );
}

export default AppDemo;
