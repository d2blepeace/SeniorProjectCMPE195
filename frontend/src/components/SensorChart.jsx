import React, {useState } from "react"; 
import "../styles/sensorChart.css";

function SensorChart({title, unit, data = []}) {

    // indicate if the card of chart is clicked or not
    const [isExpanded, setIsExpanded] = useState(false);
    const toggleExpand = () => {
        setIsExpanded((prev) => !prev);
    };

    // For the chart
    const topPadding = 15;
    const bottomPadding = 15;
    const usableHeight = 100 - topPadding - bottomPadding;

    // value of min, max and range of data
    const maxValue = Math.max(...data, 1);
    const minValue = Math.min(...data, 0);
    const range = maxValue - minValue || 1;

    const points = data.map((value, index) => {
        const x = (index / (data.length - 1 || 1)) * 100;
        const normalized = (value - minValue) / range;
        const y = topPadding + (1 - normalized) * usableHeight;
        return `${x},${y}`;
    }).join(" ");

    return (
        <div className={`sensor-chart-card ${isExpanded ? "expanded" : ""}`}
                onClick={toggleExpand}
        >   
            <div className="sensor-chart-header">
                <h3>{title}</h3>
                <span className="expand-hint">
                    {isExpanded ? "Click to collapse" : "Click to expand"}
                </span>
            </div>

            <div className="sensor-chart-body">
                <svg
                    viewBox="0 0 100 100"
                    preserveAspectRatio="none"
                    className="chart-svg"
                >
                    <polyline
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        points={points}
                    />
                </svg>
            </div>

            <div className="sensor-chart-footer">
                <span>Min: {minValue}{unit}</span>
                <span>Max: {maxValue}{unit}</span>
            </div>
        </div>
    );
} 

export default SensorChart;