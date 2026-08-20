import React, { useState } from "react"; 
import "../styles/sensorChart.css";

function SensorChart({title, unit, data = [], timestamps = []}) {
    const [isExpanded, setIsExpanded] = useState(false);
    const [hoveredPoint, setHoveredPoint] = useState(null);

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
        return { x, y, value, timestamp: timestamps[index] };
    });

    const polylinePoints = points.map(p => `${p.x},${p.y}`).join(" ");

    // Format timestamp for display
    const formatTimestamp = (timestamp) => {
    if (!timestamp) return "";
    
    // Backend sends "YYYY-MM-DD HH:MM:SS" format in UTC
    // Convert to ISO format and append 'Z' to indicate UTC
    const utcTimestamp = timestamp.replace(' ', 'T') + 'Z';
    const date = new Date(utcTimestamp);
    
    return date.toLocaleString('en-US', { 
        timeZone: 'America/Los_Angeles',
        month: 'short', 
        day: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit',
      });
    };

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
                    {/* Line chart */}
                    <polyline
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        points={polylinePoints}
                    />

                    {/* Invisible hover points */}
                    {points.map((point, index) => (
                        <circle
                            key={index}
                            cx={point.x}
                            cy={point.y}
                            r="3"
                            fill="currentColor"
                            opacity={hoveredPoint === index ? 1 : 0}
                            onMouseEnter={(e) => {
                                e.stopPropagation();
                                setHoveredPoint(index);
                            }}
                            onMouseLeave={(e) => {
                                e.stopPropagation();
                                setHoveredPoint(null);
                            }}
                            style={{ cursor: 'pointer' }}
                        />
                    ))}
                </svg>

                {/* Tooltip */}
                {hoveredPoint !== null && (
                    <div 
                        className="chart-tooltip"
                        style={{
                            left: `${points[hoveredPoint].x}%`,
                            top: `${points[hoveredPoint].y}%`
                        }}
                    >
                        <div className="tooltip-value">
                            {points[hoveredPoint].value}{unit}
                        </div>
                        <div className="tooltip-timestamp">
                            {formatTimestamp(points[hoveredPoint].timestamp)}
                        </div>
                    </div>
                )}
            </div>

            <div className="sensor-chart-footer">
                <span>Min: {minValue}{unit}</span>
                <span>Max: {maxValue}{unit}</span>
            </div>
        </div>
    );
} 

export default SensorChart;