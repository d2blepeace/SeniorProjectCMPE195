import ChartCard from "../components/ChartCard";

export default function Dashboard() {
    return (
        <div>
            <h1 className="text-3xl font-bold mb-6 text-gray-800">
        🌱 Smart Plant Dashboard
            </h1>

        {/* Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white p-6 rounded-2xl shadow hover:shadow-lg transition">
                <p className="text-gray-500">Temperature</p>
                <h2 className="text-2xl font-bold text-green-600">25°C</h2>
            </div>

            <div className="bg-white p-6 rounded-2xl shadow hover:shadow-lg transition">
                <p className="text-gray-500">Humidity</p>
                <h2 className="text-2xl font-bold text-blue-500">60%</h2>
            </div>
        </div>

        {/* Chart */}
        <div className="mt-8">
            <ChartCard />
        </div>
    </div>
    );
}