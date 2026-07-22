document.addEventListener("DOMContentLoaded", () => {
    const coinIdInput = document.getElementById("coin_id");
    const quantityInput = document.getElementById("quantity");
    const amountInput = document.getElementById("amountInput");
    const amountLabel = document.getElementById("amountLabel");
    const amountConversionEl = document.getElementById("amountConversion");
    const amountModeButtons = document.querySelectorAll("[data-amount-mode]");

    const currentPriceEl = document.getElementById("currentPrice");
    const feeEstimateEl = document.getElementById("feeEstimate");
    const totalEstimateEl = document.getElementById("totalEstimate");
    const totalLabelEl = document.getElementById("totalLabel");
    const heldQuantityEl = document.getElementById("heldQuantity");
    const actionInput = document.getElementById("actionInput");
    const submitBtn = document.getElementById("submitTradeBtn");
    const tabs = document.querySelectorAll(".trading-tab");
    const quickButtons = document.querySelectorAll(".quick-amount-btn");

    const pickerTrigger = document.getElementById("coinPickerTrigger");
    const pickerPanel = document.getElementById("coinPickerPanel");
    const pickerSearch = document.getElementById("coinPickerSearch");
    const pickerOptions = document.querySelectorAll(".coin-picker-option");
    const pickerIcon = document.getElementById("coinPickerIcon");
    const pickerName = document.getElementById("coinPickerName");
    const pickerSymbol = document.getElementById("coinPickerSymbol");
    const pickerPrice = document.getElementById("coinPickerPrice");

    const chartCanvas = document.getElementById("tradingChart");
    const chartEmptyEl = document.getElementById("tradingChartEmpty");
    const chartCoinLabelEl = document.getElementById("chartCoinLabel");

    if (!coinIdInput || !quantityInput || !amountInput) return;

    const FEE_RATE = 0.005;
    let mode = "buy";
    let amountMode = "quantity";
    let tradingChartInstance = null;

    function currentPrice() {
        return parseFloat(coinIdInput.dataset.price || "0") || 0;
    }

    function heldQuantity() {
        return (window.HOLDINGS && window.HOLDINGS[coinIdInput.value]) || 0;
    }

    function syncQuantityFromAmount() {
        const price = currentPrice();
        const rawValue = parseFloat(amountInput.value || "0") || 0;

        let quantity;
        if (amountMode === "usd") {
            quantity = price > 0 ? rawValue / price : 0;
            amountConversionEl.textContent = price > 0 ? `≈ ${quantity.toFixed(8)} unités` : "";
        } else {
            quantity = rawValue;
            amountConversionEl.textContent = price > 0 ? `≈ $${(rawValue * price).toFixed(2)}` : "";
        }

        quantityInput.value = quantity > 0 ? quantity : "";
        return quantity;
    }

    function updateEstimate() {
        const price = currentPrice();
        const quantity = syncQuantityFromAmount();

        const subtotal = price * quantity;
        const fee = subtotal * FEE_RATE;
        const total = subtotal + fee;

        currentPriceEl.textContent = price.toFixed(2);
        feeEstimateEl.textContent = fee.toFixed(2);
        totalEstimateEl.textContent = total.toFixed(2);
        heldQuantityEl.textContent = heldQuantity();
    }

    function setMode(newMode) {
        mode = newMode;
        actionInput.value = mode;
        tabs.forEach((tab) => tab.classList.toggle("active", tab.dataset.mode === mode));

        if (mode === "buy") {
            submitBtn.textContent = "Acheter";
            submitBtn.className = "btn btn-buy";
            totalLabelEl.textContent = "achat";
        } else {
            submitBtn.textContent = "Vendre";
            submitBtn.className = "btn btn-sell";
            totalLabelEl.textContent = "vente";
        }
    }

    function setAmountMode(newAmountMode) {
        const price = currentPrice();
        const currentQuantity = amountMode === "usd"
            ? (price > 0 ? (parseFloat(amountInput.value || "0") || 0) / price : 0)
            : (parseFloat(amountInput.value || "0") || 0);

        amountMode = newAmountMode;
        amountModeButtons.forEach((btn) => btn.classList.toggle("active", btn.dataset.amountMode === amountMode));

        if (amountMode === "usd") {
            amountLabel.textContent = "Montant ($)";
            amountInput.value = currentQuantity > 0 ? (currentQuantity * price).toFixed(2) : "";
        } else {
            amountLabel.textContent = "Quantité";
            amountInput.value = currentQuantity > 0 ? currentQuantity.toFixed(8) : "";
        }

        updateEstimate();
    }

    function applyQuickAmount(pct) {
        const price = currentPrice();
        if (price <= 0) return;

        let quantity;
        if (mode === "buy") {
            const spendable = ((window.CASH_BALANCE || 0) * pct) / (1 + FEE_RATE);
            quantity = spendable / price;
        } else {
            quantity = heldQuantity() * pct;
        }

        if (amountMode === "usd") {
            amountInput.value = quantity > 0 ? (quantity * price).toFixed(2) : "";
        } else {
            amountInput.value = quantity > 0 ? quantity.toFixed(8) : "";
        }
        updateEstimate();
    }

    function refreshPrice() {
        const coinId = coinIdInput.value;
        fetch(`/trading/price/${coinId}`)
            .then((res) => (res.ok ? res.json() : null))
            .then((data) => {
                if (!data || !data.price) return;
                coinIdInput.dataset.price = data.price;
                pickerPrice.textContent = `$${Number(data.price).toFixed(2)}`;
                updateEstimate();
            })
            .catch(() => {});
    }

    function selectCoin(option) {
        coinIdInput.value = option.dataset.coinId;
        coinIdInput.dataset.price = option.dataset.price;

        pickerIcon.src = option.dataset.image;
        pickerName.textContent = option.dataset.name;
        pickerSymbol.textContent = option.dataset.symbol;
        pickerPrice.textContent = `$${parseFloat(option.dataset.price).toFixed(2)}`;

        closePicker();
        updateEstimate();
        loadTradingChart(option.dataset.coinId, option.dataset.name, option.dataset.symbol);
    }

    function openPicker() {
        pickerPanel.hidden = false;
        pickerSearch.value = "";
        filterPickerOptions("");
        pickerSearch.focus();
    }

    function closePicker() {
        pickerPanel.hidden = true;
    }

    function filterPickerOptions(query) {
        const normalized = query.trim().toLowerCase();
        pickerOptions.forEach((opt) => {
            const matches = opt.dataset.search.includes(normalized);
            opt.style.display = matches ? "flex" : "none";
        });
    }

    function loadTradingChart(coinId, name, symbol) {
        if (!chartCanvas || typeof Chart === "undefined") return;

        chartCoinLabelEl.textContent = `${name} (${symbol}) — 7 derniers jours`;
        chartEmptyEl.style.display = "none";
        chartCanvas.style.display = "block";

        fetch(`/trading/chart/${coinId}`)
            .then((res) => (res.ok ? res.json() : null))
            .then((data) => {
                if (tradingChartInstance) {
                    tradingChartInstance.destroy();
                    tradingChartInstance = null;
                }

                if (!data || !data.prices || data.prices.length === 0) {
                    chartEmptyEl.style.display = "block";
                    chartCanvas.style.display = "none";
                    return;
                }

                const labels = data.prices.map((p) => {
                    const date = new Date(p[0]);
                    return date.toLocaleDateString("fr-FR", { day: "2-digit", month: "2-digit" });
                });
                const values = data.prices.map((p) => p[1]);
                const trendUp = values[values.length - 1] >= values[0];
                const lineColor = trendUp ? "#16a34a" : "#dc2626";
                const fillColor = trendUp ? "rgba(22, 163, 74, 0.08)" : "rgba(220, 38, 38, 0.08)";

                const datasets = [{
                    label: "Prix",
                    data: values,
                    borderColor: lineColor,
                    backgroundColor: fillColor,
                    fill: true,
                    tension: 0.25,
                    pointRadius: 0,
                    borderWidth: 2,
                }];

                if (data.avg_buy_price) {
                    datasets.push({
                        label: "Votre prix d'entrée",
                        data: values.map(() => data.avg_buy_price),
                        borderColor: "#6b7280",
                        borderDash: [6, 4],
                        borderWidth: 1.5,
                        pointRadius: 0,
                        fill: false,
                    });
                }

                tradingChartInstance = new Chart(chartCanvas, {
                    type: "line",
                    data: { labels, datasets },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { display: datasets.length > 1, labels: { color: "#111827", boxWidth: 12 } },
                        },
                        scales: {
                            x: { ticks: { color: "#6b7280", maxTicksLimit: 6 }, grid: { display: false } },
                            y: { ticks: { color: "#6b7280" }, grid: { color: "#e5e8ef" } },
                        },
                    },
                });
            })
            .catch(() => {
                chartEmptyEl.style.display = "block";
                chartCanvas.style.display = "none";
            });
    }

    tabs.forEach((tab) => {
        tab.addEventListener("click", () => setMode(tab.dataset.mode));
    });

    amountModeButtons.forEach((btn) => {
        btn.addEventListener("click", () => setAmountMode(btn.dataset.amountMode));
    });

    quickButtons.forEach((btn) => {
        btn.addEventListener("click", () => applyQuickAmount(parseFloat(btn.dataset.pct)));
    });

    if (pickerTrigger) {
        pickerTrigger.addEventListener("click", () => {
            if (pickerPanel.hidden) {
                openPicker();
            } else {
                closePicker();
            }
        });
    }

    if (pickerSearch) {
        pickerSearch.addEventListener("input", () => filterPickerOptions(pickerSearch.value));
    }

    pickerOptions.forEach((opt) => {
        opt.addEventListener("click", () => selectCoin(opt));
    });

    document.addEventListener("click", (event) => {
        if (!pickerPanel.hidden && !event.target.closest(".coin-picker")) {
            closePicker();
        }
    });

    setMode(window.INITIAL_MODE === "sell" ? "sell" : "buy");

    amountInput.addEventListener("input", updateEstimate);
    updateEstimate();

    // Initialise le picker et le graphique avec la crypto déjà sélectionnée côté serveur
    const initialOption = document.querySelector(
        `.coin-picker-option[data-coin-id="${coinIdInput.value}"]`
    ) || pickerOptions[0];
    if (initialOption) {
        selectCoin(initialOption);
    }

    setInterval(refreshPrice, 15000);
});
