/**
 * Tab switcher to switch between Dashboard and Setting
 * 
 * Props:
 *  - activeTab: "dashboard" | "settings"
 *  - onTabChange: function(tabName)
 */

import React from "react";
import "../styles/tabBar.css";

function TabBar({activeTab, onTabChange}) {
    return (
        <nav className="tab-bar">
            {/* Dashboard Tab */}
            <button
                className={`tab-btn ${activeTab === "dashboard" ? "active" : ""}`}
                onClick={() => onTabChange("dashboard")}
            >
                DashBoard
            </button>

            {/* SettingsTab */}
            <button
                className={`tab-btn ${activeTab === "settings" ? "active" : ""}`}
                onClick={() => onTabChange("settings")}
            >
                Settings
            </button>
        </nav>
    );
}

export default TabBar;


