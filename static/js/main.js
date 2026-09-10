/**
 * DriveWorth - Global Main JavaScript
 */

document.addEventListener("DOMContentLoaded", () => {
    // Mobile Hamburger Menu Toggle
    const mobileToggle = document.getElementById("mobileToggle");
    const navMenu = document.getElementById("navMenu");

    if (mobileToggle && navMenu) {
        mobileToggle.addEventListener("click", () => {
            navMenu.classList.toggle("show");
        });
    }

    // Fetch Database & Home Stats if on homepage
    fetchSystemStats();
});

async function fetchSystemStats() {
    try {
        const res = await fetch("/api/stats");
        const json = await res.json();
        
        if (json.success && json.data) {
            const data = json.data;

            // Update homepage counters if elements exist
            const elCars = document.getElementById("statCars");
            const elBrands = document.getElementById("statBrands");
            const elDbStatus = document.getElementById("dbStatusText");

            if (elCars) elCars.innerText = `${data.total_cars.toLocaleString('en-IN')}+`;
            if (elBrands) elBrands.innerText = `${data.total_brands}+`;
            if (elDbStatus) elDbStatus.innerText = data.db_status || "System Operational";
        }
    } catch (err) {
        console.warn("Unable to fetch system stats:", err);
    }
}
