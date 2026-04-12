import React from "react";
import "../styles/sensorCard.css";

/**
 * Sensor card will be use to display: 
 *  temp: C
 *  Humidity: %
 *  pH: double
 *  status: Normal/Warning/Danger
 */


function SensorCard({title, value, unit, min, max}) {
    let status = "normal";
    const rangeBuffer = (max - min)*0.1;
    const currentValue = Number(value);
    const minVal = Number(min);
    const maxVal = Number(max);

    // Condition for Danger (either < min or > max)
    if (value < minVal || value > maxVal) {
        status = "danger";
    } 
    // condition for "warning": only close to edge of min or max
    else if ( value <= minVal + rangeBuffer || value >= maxVal - rangeBuffer) {
        status = "warning";
    } else {
        status = "normal";
    }

    return (
        <div className={`sensor-card ${status}`}>
            <h3>{title}</h3>
            <p className="sensor-value">
                {currentValue} {unit}
            </p>
            <p className="sensor-status">{status.toUpperCase()}</p>
        </div>
    );
}
export default SensorCard;
