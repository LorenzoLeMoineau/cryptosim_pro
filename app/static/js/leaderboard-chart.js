document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("leaderboardChart");
    if (!canvas || typeof Chart === "undefined") return;

    new Chart(canvas, {
        type: "bar",
        data: {
            labels: window.CHART_LABELS || [],
            datasets: [{
                label: "Valeur du portefeuille ($)",
                data: window.CHART_VALUES || [],
                backgroundColor: "#6366f1",
                borderRadius: 4,
            }],
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
            },
            scales: {
                x: { ticks: { color: "#8b8fa3" }, grid: { color: "#2a2e3f" } },
                y: { ticks: { color: "#8b8fa3" }, grid: { color: "#2a2e3f" } },
            },
        },
    });
});
