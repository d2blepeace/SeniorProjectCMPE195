import { useState } from "react";
import "./styles/App.css";

import Navbar from "./components/Navbar.jsx";
import SensorCard from "./components/SensorCard.jsx";
import SensorChart from "./components/SensorChart.jsx";
import TabBar from "./components/TabBar.jsx";
import Settings from "./pages/Settings.jsx";

import useDashboardData from "./hooks/useDashboardData.js";


function App() {
    const { device, current, thresholds, charts, loading, error } = useDashboardData();

    // "dashboard" = show sensor cards and charts
    // "settings"  = show threshold profile management
    const [activeTab, setActiveTab] = useState("dashboard");

    // Loading State 
    if (loading) {
        return (
            <>
                <Navbar deviceName="Loading..." status="offline" />
                <TabBar activeTab={activeTab} onTabChange={setActiveTab} />
                <main className="dashboard">
                    {activeTab === "dashboard" ? (
                        <p>Loading dashboard data...</p>
                    ) : (
                        <Settings />
                    )}
                </main>
            </>
        );
    }

    // Error State 
    if (error) {
        return (
            <>
                <Navbar deviceName="System Error" status="offline" />
                <TabBar activeTab={activeTab} onTabChange={setActiveTab} />
                <main className="dashboard">
                    {activeTab === "dashboard" ? (
                        <p>Error: {error}</p>
                    ) : (
                        <Settings />
                    )}
                </main>
            </>
        );
    }

    //  Main Render 
    return (
        <>
            {/* Navbar - always visible */}
            <Navbar
                deviceName={device?.name || "Smart Hydroponic System"}
                status={device?.status || "offline"}
                lastUpdated={device?.lastUpdated}
            />

            {/* Tab Bar - always visible, switches between pages */}
            <TabBar activeTab={activeTab} onTabChange={setActiveTab} />

            {/*
             * Page Content - conditionally rendered based on active tab
             *
             * Dashboard tab: shows the existing sensor cards and charts
             * Settings tab: shows the profile management page
             */}
            {activeTab === "dashboard" ? (
                //  Dashboard Content (original code, unchanged) ──
                <main className="dashboard">
                    <section className="card-grid">
                        <SensorCard
                            title="Temperature"
                            value={current?.temperature ?? 0}
                            unit=" °C"
                            min={thresholds?.temperature?.min ?? 0}
                            max={thresholds?.temperature?.max ?? 0}
                        />
                        <SensorCard
                            title="Humidity"
                            value={current?.humidity ?? 0}
                            unit=" %"
                            min={thresholds?.humidity?.min ?? 0}
                            max={thresholds?.humidity?.max ?? 0}
                        />
                        <SensorCard
                            title="pH"
                            value={current?.ph ?? 0}
                            unit=""
                            min={thresholds?.ph?.min ?? 0}
                            max={thresholds?.ph?.max ?? 0}
                        />
                    </section>

                    <section className="sensor-chart-grid" style={{ marginTop: "40px" }}>
                        <SensorChart
                            title="Temperature Chart"
                            unit="°C"
                            data={charts?.temperature?.data ?? []}
                        />
                        <SensorChart
                            title="Humidity Chart"
                            unit="%"
                            data={charts?.humidity?.data ?? []}
                        />
                        <SensorChart
                            title="pH Chart"
                            unit=""
                            data={charts?.ph?.data ?? []}
                        />
                    </section>
                </main>
            ) : (
                //  Settings Page
                <main className="dashboard">
                    <Settings />
                </main>
            )}
        </>
    );
}

export default App;