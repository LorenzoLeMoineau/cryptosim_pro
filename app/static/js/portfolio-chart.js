document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById("allocationChart");
    if (!canvas || typeof Chart === "undefined") return;

    const PALETTE = [
        "#6366f1", "#16c784", "#ea3943", "#f5b400",
        "#06b6d4", "#a855f7", "#f97316", "#84cc16",
        "#ec4899", "#14b8a6", "#eab308", "#3b82f6",
    ];

    // Couleur dérivée du nom de la crypto (pas de sa position dans le tableau)
    // pour qu'une crypto garde la même couleur d'un portefeuille à l'autre,
    // avec résolution des collisions pour garantir des couleurs uniques
    // entre les cryptos affichées dans un même graphique.
    function assignColors(labels) {
        const used = new Set();

        return labels.map((label) => {
            let hash = 0;
            for (let i = 0; i < label.length; i++) {
                hash = (hash * 31 + label.charCodeAt(i)) | 0;
            }

            let index = Math.abs(hash) % PALETTE.length;
            let attempts = 0;
            while (used.has(index) && attempts < PALETTE.length) {
                index = (index + 1) % PALETTE.length;
                attempts++;
            }

            used.add(index);
            return PALETTE[index];
        });
    }

    const labels = window.CHART_LABELS || [];

    new Chart(canvas, {
        type: "doughnut",
        data: {
            labels,
            datasets: [{
                data: window.CHART_VALUES || [],
                backgroundColor: assignColors(labels),
                borderColor: "#ffffff",
                borderWidth: 2,
            }],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "bottom",
                    labels: { color: "#111827" },
                },
            },
        },
    });
});
