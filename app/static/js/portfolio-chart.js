document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("allocationChart");
    if (!canvas || typeof Chart === "undefined") return;

    const PALETTE = [
        "#6366f1", "#16c784", "#ea3943", "#f5b400",
        "#06b6d4", "#a855f7", "#f97316", "#84cc16",
        "#ec4899", "#14b8a6", "#eab308", "#3b82f6",
    ];

    // Couleur dérivée du nom de la crypto (et non de sa position dans le tableau)
    // pour qu'une crypto garde toujours la même couleur d'un portefeuille à l'autre.
    function colorForLabel(label) {
        let hash = 0;
        for (let i = 0; i < label.length; i++) {
            hash = (hash * 31 + label.charCodeAt(i)) | 0;
        }
        return PALETTE[Math.abs(hash) % PALETTE.length];
    }

    const labels = window.CHART_LABELS || [];

    new Chart(canvas, {
        type: "doughnut",
        data: {
            labels,
            datasets: [{
                data: window.CHART_VALUES || [],
                backgroundColor: labels.map(colorForLabel),
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
