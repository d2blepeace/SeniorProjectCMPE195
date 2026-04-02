/**
 * this service layer will talk to backend, it should do:
 *  - fetch from backend
 *  - handle errors
 *  - wrap endpoints
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function fetchJSON(endpoint, options = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {}),
        },
        ...options,
    });

    if (!response.ok) {
        let message = `Request failed with status ${response.status}`;

        try {
            const errorData = await response.json();
            if (errorData?.detail) {
                message = errorData.detail;
            }
        } catch {
            // ignore JSON parse errors
        }

        throw new Error(message);
    }

    return response.json();
}

// Health and System
export async function fetchHealth() {
    return fetchJSON("/api/health");
}

export async function fetchSystemStatus() {
    return fetchJSON("/api/status");
}

// Sensors
export async function fetchCurrentReadings() {
    return fetchJSON("/api/sensors/current");
}

export async function fetchLatestReadings() {
    return fetchJSON("/api/sensors/latest");
}

export async function fetchHistoricalData({
    hours = 24,
    limit = 200,
    sensorType = null,
} = {}) {
    const params = new URLSearchParams();

    params.set("hours", String(hours));
    params.set("limit", String(limit));

    if (sensorType) {
        params.set("sensor_type", sensorType);
    }

    return fetchJSON(`/api/sensors/historical?${params.toString()}`);
}

export async function fetchSensorStatus() {
    return fetchJSON("/api/sensors/status");
}

// Configurations
export async function fetchAllConfigurations() {
    return fetchJSON("/api/configurations/");
}

export async function fetchActiveConfiguration() {
    return fetchJSON("/api/configurations/active");
}

// Optional startup helper
export async function fetchDashboardBootstrap() {
    const [systemStatus, latestReadings, activeConfiguration] =
        await Promise.all([
            fetchSystemStatus(),
            fetchLatestReadings(),
            fetchActiveConfiguration(),
        ]);

    return {
        systemStatus,
        latestReadings,
        activeConfiguration,
    };
}