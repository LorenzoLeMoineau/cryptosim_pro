document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("navbarToggle");
    const links = document.getElementById("navbarLinks");

    if (toggle && links) {
        toggle.addEventListener("click", () => {
            links.classList.toggle("open");
        });
    }

    // Rend les tableaux scrollables horizontalement sur mobile sans toucher aux templates
    document.querySelectorAll("table").forEach((table) => {
        if (table.parentElement.classList.contains("table-wrap")) return;
        const wrapper = document.createElement("div");
        wrapper.className = "table-wrap";
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
    });

    // Indicateur de chargement sur les formulaires pour éviter les doubles soumissions
    document.querySelectorAll("form").forEach((form) => {
        form.addEventListener("submit", (event) => {
            const submitBtn = event.submitter || form.querySelector("button[type='submit']");
            if (submitBtn && !submitBtn.disabled) {
                setTimeout(() => {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<span class="loading"></span> Chargement...';
                }, 0);
            }
        });
    });

    // Notifications toast (alertes de prix) : fermeture manuelle + auto-dismiss
    document.querySelectorAll(".toast").forEach((toast, index) => {
        const dismiss = () => {
            toast.classList.add("toast-hide");
            toast.addEventListener("animationend", () => toast.remove(), { once: true });
        };

        const closeBtn = toast.querySelector(".toast-close");
        if (closeBtn) closeBtn.addEventListener("click", dismiss);

        setTimeout(dismiss, 8000 + index * 400);
    });
});
