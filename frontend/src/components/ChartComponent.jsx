import { Line } from "react-chartjs-2";
import {
    Chart as ChartJS,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
} from "chart.js";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

export default function ChartComponent() {
    const data = {
        labels: ["Mon", "Tue", "Wed", "Thu", "Fri"],
        datasets: [
            {
                label: "Temperature",
                data: [22, 24, 23, 25, 26],
                borderColor: "#16a34a",
                fill: true,
            },
        ],
    };

    return <Line data={data} />;
}