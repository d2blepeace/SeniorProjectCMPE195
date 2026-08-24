import { useState } from "react";
import "./styles/App.css";

import Navbar from "./components/Navbar.jsx";
import TabBar from "./components/TabBar.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Settings from "./pages/Settings.jsx";

import useDashboardData from "./hooks/useDashboardData.js";


function App() {
    const { device, current, thresholds, charts, loading, error } = useDashboardData();

    // "dashboard" = show sensor cards and charts
    // "settings"  = show threshold profile management
    const [activeTab, setActiveTab] = useState("dashboard");

    // Dark / Light mode
    const [darkMode, setDarkMode] = useState(false);
    // Loading State
    if (loading) {
        return (
            <>
                <Navbar 
                    deviceName="Loading..." 
                    status="offline" 
                    darkMode={darkMode} 
                    onToggleDarkMode={() => setDarkMode(!darkMode)}
                />
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
                <Navbar 
                    deviceName="System Error" 
                    status="offline"
                    darkMode={darkMode}
                    onToggleDarkMode={() => setDarkMode(!darkMode)}
                />
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

    // Main Render
    return (
        <>
            {/* Navbar - always visible */}
            <Navbar
                deviceName={device?.name || "Smart Hydroponic System"}
                status={device?.status || "offline"}
                lastUpdated={device?.lastUpdated}
                darkMode={darkMode}
                onToggleDarkMode={() => setDarkMode(!darkMode)}
            />

            {/* Tab Bar - always visible, switches between pages */}
            <TabBar activeTab={activeTab} onTabChange={setActiveTab} />

            {/*Page Content - conditionally rendered based on active tab*/}
            {activeTab === "dashboard" ? (
                <Dashboard
                    current={current}
                    thresholds={thresholds}
                    charts={charts}
                />
            ) : (
                <main className="dashboard">
                    <Settings />
                </main>
            )}
        </>
    );
}

export default App;
