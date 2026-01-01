import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import {
    Chart as ChartJS,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Tooltip,
    Legend,
} from "chart.js";
import { useAuth } from "../../context/auth";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend);

const EmotionShow=()=>{
    const [data, setData] = useState([]);
    const [currentWeek, setCurrentWeek] = useState(0);
    const itemsPerWeek = 4; // Show 4 data points per page (roughly a week)
    const [auth,setAuth]=useAuth();
    useEffect(() => {
        fetch("http://127.0.0.1:5000/api/v1/emotion-history",{
            method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: auth.user["_id"] })
        })
            .then((res) => res.json())
            .then((data) => {
                // Sort by date (ascending)
                const sorted = data.sort(
                    (a, b) =>
                        new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
                );
                setData(sorted);
            });
    }, []);

    const totalWeeks = Math.ceil(data.length / itemsPerWeek);
    const startIndex = currentWeek * itemsPerWeek;
    const endIndex = startIndex + itemsPerWeek;
    const weekData = data.slice(startIndex, endIndex);

    const chartData = {
        labels: weekData.map((d) => new Date(d.timestamp).toLocaleDateString()),
        datasets: [
            {
                label: `Emotion Progress (Week ${currentWeek + 1}/${totalWeeks})`,
                data: weekData.map((d) => d.emotion_score),
                borderColor: "#0d6efd",
                backgroundColor: "rgba(13, 110, 253, 0.2)",
                borderWidth: 3,
                pointBackgroundColor: "#0d6efd",
                fill: true,
                tension: 0.3,
            },
        ],
    };

    const handleNext = () => {
        if (currentWeek < totalWeeks - 1) setCurrentWeek(currentWeek + 1);
    };

    const handlePrev = () => {
        if (currentWeek > 0) setCurrentWeek(currentWeek - 1);
    };

    return (
        <div className="container py-5">
            <div className="text-center mb-4">
                <h2 className="fw-bold text-primary">🧘 Emotion Growth Tracker</h2>
                <p className="text-secondary">
                    Weekly emotional progress based on user interactions
                </p>
            </div>

            <div style={{ position: "relative", width: "100%", height: "400px" }}>
                {weekData.length > 0 ? (
                    <Line data={chartData}  options={{
                        responsive: true, maintainAspectRatio: false,
                        scales: {y: {beginAtZero: true,max: 1,ticks: { stepSize: 0.2 },},},
                        plugins: {legend: {display: true,position: "bottom",},},
                    }} />
                ) : (
                    <p className="text-center text-muted">Loading data...</p>
                )}
            </div>

            {/* Navigation Buttons */}
            <div className="d-flex justify-content-center align-items-center mt-4 gap-3">
                <button
                    className="btn btn-outline-primary"
                    onClick={handlePrev}
                    disabled={currentWeek === 0}
                >
                    ⬅️ Previous
                </button>
                <span className="fw-semibold text-secondary">
                    Week {currentWeek + 1} of {totalWeeks}
                </span>
                <button
                    className="btn btn-outline-primary"
                    onClick={handleNext}
                    disabled={currentWeek === totalWeeks - 1}
                >
                    Next ➡️
                </button>
            </div>

            {/* Latest Emotion Info */}
            {weekData.length > 0 && (
                <div className="text-center mt-4">
                    <h5 className="text-success fw-semibold">
                        Latest Emotion:{" "}
                        <span className="text-capitalize">{weekData[weekData.length - 1].emotion}</span>
                    </h5>
                </div>
            )}
        </div>
    );
}

export default EmotionShow;
