document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("marketSearch");
    const rows = document.querySelectorAll(".market-row");
    const noResults = document.getElementById("noResults");

    if (!searchInput) return;

    searchInput.addEventListener("input", () => {
        const query = searchInput.value.trim().toLowerCase();
        let visibleCount = 0;

        rows.forEach((row) => {
            const matches = row.dataset.name.includes(query);
            row.style.display = matches ? "" : "none";
            if (matches) visibleCount += 1;
        });

        if (noResults) {
            noResults.style.display = visibleCount === 0 ? "block" : "none";
        }
    });
});
