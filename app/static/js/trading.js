document.addEventListener("DOMContentLoaded", () => {
    const coinSelect = document.getElementById("coin_id");
    const quantityInput = document.getElementById("quantity");
    const currentPriceEl = document.getElementById("currentPrice");
    const feeEstimateEl = document.getElementById("feeEstimate");
    const totalEstimateEl = document.getElementById("totalEstimate");
    const totalLabelEl = document.getElementById("totalLabel");
    const heldQuantityEl = document.getElementById("heldQuantity");
    const actionInput = document.getElementById("actionInput");
    const submitBtn = document.getElementById("submitTradeBtn");
    const tabs = document.querySelectorAll(".trading-tab");
    const quickButtons = document.querySelectorAll(".quick-amount-btn");

    if (!coinSelect || !quantityInput) return;

    const FEE_RATE = 0.005;
    let mode = "buy";

    function currentPrice() {
        const selectedOption = coinSelect.options[coinSelect.selectedIndex];
        return parseFloat(selectedOption ? selectedOption.dataset.price : "0") || 0;
    }

    function heldQuantity() {
        return (window.HOLDINGS && window.HOLDINGS[coinSelect.value]) || 0;
    }

    function updateEstimate() {
        const price = currentPrice();
        const quantity = parseFloat(quantityInput.value || "0") || 0;

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
        quantityInput.value = quantity > 0 ? quantity.toFixed(8) : "";
        updateEstimate();
    }

    function refreshPrice() {
        const coinId = coinSelect.value;
        fetch(`/trading/price/${coinId}`)
            .then((res) => (res.ok ? res.json() : null))
            .then((data) => {
                if (!data || !data.price) return;
                const selectedOption = coinSelect.options[coinSelect.selectedIndex];
                if (selectedOption) {
                    selectedOption.dataset.price = data.price;
                }
                updateEstimate();
            })
            .catch(() => {});
    }

    tabs.forEach((tab) => {
        tab.addEventListener("click", () => setMode(tab.dataset.mode));
    });

    quickButtons.forEach((btn) => {
        btn.addEventListener("click", () => applyQuickAmount(parseFloat(btn.dataset.pct)));
    });

    coinSelect.addEventListener("change", updateEstimate);
    quantityInput.addEventListener("input", updateEstimate);
    updateEstimate();

    setInterval(refreshPrice, 15000);
});
