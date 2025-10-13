document.addEventListener("DOMContentLoaded", () => {
    const countdownEl = document.getElementById("countdown");
    const orderTimeEl = document.getElementById("order-time");
    const toggleBtn = document.getElementById("toggle-update");
    const updateForm = document.getElementById("update-form");

    // Countdown timer logic
    if (countdownEl && orderTimeEl) {
        const orderTime = new Date(orderTimeEl.textContent);
        const shipDelayMs = 2 * 60 * 1000; // 2 minutes for testing
        const shipTime = new Date(orderTime.getTime() + shipDelayMs);

        const updateCountdown = () => {
            const now = new Date();
            const diff = shipTime - now;

            if (diff <= 0) {
                countdownEl.textContent = "Order Shipped!";
                clearInterval(timer);
                return;
            }

            const minutes = Math.floor(diff / 60000);
            const seconds = Math.floor((diff % 60000) / 1000);
            countdownEl.textContent = `${minutes}m ${seconds}s until shipment`;
        };

        updateCountdown();
        const timer = setInterval(updateCountdown, 1000);
    }

    // Toggle update form
    if (toggleBtn && updateForm) {
        toggleBtn.addEventListener("click", () => {
            const visible = updateForm.style.display === "block";
            updateForm.style.display = visible ? "none" : "block";
            toggleBtn.textContent = visible ? "Update Shipping" : "Cancel Update";
        });
    }
});
