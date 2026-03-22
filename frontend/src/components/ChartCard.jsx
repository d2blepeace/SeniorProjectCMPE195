import ChartComponent from "./ChartComponent";

export default function ChartCard() {
    return (
        <div className="bg-white p-6 rounded-2xl shadow hover:shadow-lg transition">
            <h3 className="text-lg font-semibold mb-4 text-gray-700">
                📊 Temperature Trend
            </h3>
            <ChartComponent />
        </div>
    );
}