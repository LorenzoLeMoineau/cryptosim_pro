document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("allocationChart");
    if (!canvas || typeof Chart === "undefined") return;

    new Chart(canvas, {
        type: "doughnut",
        data: {
            labels: window.CHART_LABELS || [],
            datasets: [{
                data: window.CHART_VALUES || [],
                backgroundColor: [
                    "#6366f1", "#16c784", "#ea3943", "#f5b400",
                    "#06b6d4", "#a855f7", "#f97316", "#84cc16",
                ],
                borderColor: "#1a1d29",
                borderWidth: 2,
            }],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "bottom",
                    labels: { color: "#e8e9ed" },
                },
            },
        },
    });
});
