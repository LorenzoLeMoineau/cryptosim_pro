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
                backgroundColor: "#2563eb",
                borderRadius: 4,
            }],
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
            },
            scales: {
                x: { ticks: { color: "#6b7280" }, grid: { color: "#e5e8ef" } },
                y: { ticks: { color: "#6b7280" }, grid: { color: "#e5e8ef" } },
            },
        },
    });
});
