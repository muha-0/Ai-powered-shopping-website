document.addEventListener("DOMContentLoaded", () => {
    const countdownEl = document.getElementById("countdown");
    const orderTimeEl = document.getElementById("order-time");
    const toggleBtn = document.getElementById("toggle-update");
    const updateForm = document.getElementById("update-form");

    // Countdown timer logic
    if (countdownEl && orderTimeEl) {
        const orderTime = new Date(orderTimeEl.textContent);
        console.log(orderTime);
        const shipDelayMs = 2 * 60 * 1000; // 2 minutes
        const shipTime = new Date(orderTime.getTime() + shipDelayMs);
        console.log(shipTime);
        const updateCountdown = () => {
            // This is wierd and I spent an hour debugging it
            // using new Date() returns local time so I had to convert it to UTC
            // I always prefer UTC because client can't be trusted
            // They can change their local clock and fool me
            const now = new Date();
            const nowUtc = new Date(
                now.getTime() + now.getTimezoneOffset() * 60000
            );
            const diff = shipTime - nowUtc;

            if (diff <= 0) {
                countdownEl.textContent = "Order Shipped!";
                const cancelBtn = document.getElementById("cancel-btn");
                const toggleBtn = document.getElementById("toggle-update");

                toggleBtn.disabled = true;
                cancelBtn.disabled = true;

                document.getElementById("status-cell").textContent = "Shipped";

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
            const visible = updateForm.style.display === "flex";
            updateForm.style.display = visible ? "none" : "flex";
            toggleBtn.textContent = visible ? "Update Shipping" : "Cancel Update";
        });
    }
});
