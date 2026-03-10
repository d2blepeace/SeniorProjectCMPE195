/**
 * Navigation Bar will display
 * - First row: Project Title
 * - Second row: 
 *      - Left Side: Device name: <StatusIcon> [Online | Offline]
 *      - Right Side: Latest Update: [Timestamp]
 */
import React from "react";
import onlineIcon from "../assets/icons/online.png"
import offlineIcon from "../assets/icons/offline.png"
import "../styles/typography.css"
import "../styles/navbar.css"


function Navbar({deviceName, status, lastUpdated}) {
    {/*Determine the status icon based on the connection status*/}
    const statusIcon = status === "online" ? onlineIcon : offlineIcon;

    return (
        <nav className="navbar">
            {/* TITLE */}
            <div className="nav-title">
                Smart Hydroponic Gardening System
            </div>

            {/* INFO */}
            <div className="nav-info">
                {/*NAME OF DEVICE*/}
                <div className="nav-item">
                    <span>{deviceName}</span>
                </div>

                {/* status icon and status of device*/}
                <div className="nav-item">
                    <img src={statusIcon} alt="status" />
                    <span>{status}</span>
                </div>
                
                {/*Last Update with timestamp*/}
                <div className="nav-item">
                    <span>Last update: {lastUpdated}</span>
                </div>
            </div>
        </nav>
    );
}

export default Navbar;