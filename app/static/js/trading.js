document.addEventListener("DOMContentLoaded", () => {
    const coinSelect = document.getElementById("coin_id");
    const quantityInput = document.getElementById("quantity");
    const currentPriceEl = document.getElementById("currentPrice");
    const feeEstimateEl = document.getElementById("feeEstimate");
    const totalEstimateEl = document.getElementById("totalEstimate");
    const heldQuantityEl = document.getElementById("heldQuantity");

    const FEE_RATE = 0.005;

    function updateEstimate() {
        const selectedOption = coinSelect.options[coinSelect.selectedIndex];
        const price = parseFloat(selectedOption ? selectedOption.dataset.price : "0") || 0;
        const quantity = parseFloat(quantityInput.value || "0") || 0;

        const subtotal = price * quantity;
        const fee = subtotal * FEE_RATE;
        const total = subtotal + fee;

        currentPriceEl.textContent = price.toFixed(2);
        feeEstimateEl.textContent = fee.toFixed(2);
        totalEstimateEl.textContent = total.toFixed(2);

        const held = (window.HOLDINGS && window.HOLDINGS[coinSelect.value]) || 0;
        heldQuantityEl.textContent = held;
    }

    if (coinSelect && quantityInput) {
        coinSelect.addEventListener("change", updateEstimate);
        quantityInput.addEventListener("input", updateEstimate);
        updateEstimate();
    }
});
