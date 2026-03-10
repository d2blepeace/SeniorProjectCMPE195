/**
 * Navigation Bar will display
 * - First row: Project Title
 * - Second row: 
 *      - Left Side: Device name: <StatusIcon> [Online | Offline]
 *      - Right Side: Latest Update: [Timestamp]
 */
import React from "react";
import onlineIcon from "../assets/online.png"
import offlineIcon from "../assets/offline.png"
import "./styles/typography.css"
import "./style/navbar.css"


function Navbar({deviceName, status, lastUpdated}) {
    const statusIcon = status === "online" ? onlineIcon : offlineIcon;

    return (
        <nav className="navbar">
            // TITLE
            <div className="nav-title">
                Smart Hydroponic Gardening System
            </div>

            // INFO ROW
            <div className="nav-info">
                // name of device
                <div className="nav-item">
                    <span>{deviceName}</span>
                </div>

                // status icon and status of device
                <div className="nav-item">
                    <img src={statusIcon} alt="status" />
                    <span>{status}</span>
                </div>

                // Last Update with timestamp
                <div className="nav-item">
                    <span>Last update: {lastUpdated}</span>
                </div>
            </div>
        </nav>
    );
}

export default Navbar;