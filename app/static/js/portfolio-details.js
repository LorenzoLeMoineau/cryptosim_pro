document.addEventListener("DOMContentLoaded", () => {
    const toggles = document.querySelectorAll(".position-details-toggle");
    const loadedCharts = {};

    toggles.forEach((btn) => {
        btn.addEventListener("click", () => {
            const coinId = btn.dataset.coinId;
            const row = document.getElementById(`details-row-${coinId}`);
            if (!row) return;

            const isHidden = row.style.display === "none" || !row.style.display;
            row.style.display = isHidden ? "table-row" : "none";
            btn.textContent = isHidden ? "Masquer" : "Détails";

            if (isHidden && !loadedCharts[coinId]) {
                loadedCharts[coinId] = true;
                loadPositionChart(coinId);
            }
        });
    });

    function loadPositionChart(coinId) {
        const canvas = document.getElementById(`chart-${coinId}`);
        const wrap = canvas ? canvas.closest(".position-chart-wrap") : null;
        const emptyMsg = wrap ? wrap.querySelector(".position-chart-empty") : null;

        fetch(`/portfolio/chart/${coinId}`)
            .then((res) => (res.ok ? res.json() : null))
            .then((data) => {
                if (!data || !data.prices || data.prices.length === 0 || typeof Chart === "undefined") {
                    if (emptyMsg) emptyMsg.style.display = "block";
                    if (canvas) canvas.style.display = "none";
                    return;
                }

                const labels = data.prices.map((p) => {
                    const date = new Date(p[0]);
                    return date.toLocaleDateString("fr-FR", { day: "2-digit", month: "2-digit" });
                });
                const values = data.prices.map((p) => p[1]);
                const avgBuyPrice = data.avg_buy_price;
                const lastPrice = values[values.length - 1];
                const isPositive = lastPrice >= avgBuyPrice;
                const lineColor = isPositive ? "#16a34a" : "#dc2626";
                const fillColor = isPositive ? "rgba(22, 163, 74, 0.08)" : "rgba(220, 38, 38, 0.08)";

                new Chart(canvas, {
                    type: "line",
                    data: {
                        labels,
                        datasets: [
                            {
                                label: "Prix",
                                data: values,
                                borderColor: lineColor,
                                backgroundColor: fillColor,
                                fill: true,
                                tension: 0.25,
                                pointRadius: 0,
                                borderWidth: 2,
                            },
                            {
                                label: "Prix d'entrée",
                                data: values.map(() => avgBuyPrice),
                                borderColor: "#6b7280",
                                borderDash: [6, 4],
                                borderWidth: 1.5,
                                pointRadius: 0,
                                fill: false,
                            },
                        ],
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { display: true, labels: { color: "#111827", boxWidth: 12 } },
                        },
                        scales: {
                            x: { ticks: { color: "#6b7280", maxTicksLimit: 6 }, grid: { display: false } },
                            y: { ticks: { color: "#6b7280" }, grid: { color: "#e5e8ef" } },
                        },
                    },
                });
            })
            .catch(() => {
                if (emptyMsg) emptyMsg.style.display = "block";
                if (canvas) canvas.style.display = "none";
            });
    }
});
