/**
 * DriveWorth - Admin Portal JavaScript
 */

let adminCurrentPage = 1;

document.addEventListener("DOMContentLoaded", () => {
    loadAdminStats();
    loadAdminInventory(1);
    setupAdminTabs();
    setupAdminAddCarForm();
    setupAdminSearch();
    setupAdminLogout();
});

function setupAdminLogout() {
    const logoutBtn = document.getElementById("adminLogoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", async () => {
            if (confirm("Are you sure you want to log out of Admin Dashboard?")) {
                try {
                    await fetch("/api/admin/logout", { method: "POST" });
                } catch (e) {}
                window.location.href = "/admin/login";
            }
        });
    }
}

async function loadAdminStats() {
    try {
        const res = await fetch("/api/stats");
        const json = await res.json();
        if (json.success && json.data) {
            const d = json.data;
            document.getElementById("adminTotalCars").innerText = d.total_cars.toLocaleString('en-IN');
            document.getElementById("adminTotalBrands").innerText = d.total_brands;
            document.getElementById("adminAvgPrice").innerText = d.formatted_avg_price;
            document.getElementById("adminTopFuel").innerText = d.top_fuel_type;
        }
    } catch (e) {
        console.error("Error loading admin stats:", e);
    }
}

async function loadAdminInventory(page = 1) {
    adminCurrentPage = page;
    const search = document.getElementById("adminSearchInput")?.value.trim() || "";

    try {
        const res = await fetch(`/api/cars?page=${page}&limit=10&search=${encodeURIComponent(search)}`);
        const json = await res.json();

        if (json.success && json.data) {
            renderAdminTable(json.data.cars);
            renderAdminPagination(json.data.page, json.data.pages);
        }
    } catch (e) {
        console.error("Error loading admin inventory:", e);
    }
}

function renderAdminTable(cars) {
    const tbody = document.getElementById("adminTableBody");
    if (!tbody) return;

    if (!cars || cars.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center text-secondary">No inventory listings found.</td></tr>';
        return;
    }

    tbody.innerHTML = cars.map(car => `
        <tr>
            <td><strong>${car.brand} ${car.model}</strong><br><small class="text-secondary">${car.variant || 'Standard'}</small></td>
            <td>${car.year}</td>
            <td>${car.fuel_type}</td>
            <td>${car.transmission}</td>
            <td>${car.km_driven.toLocaleString('en-IN')} km</td>
            <td>${car.location}</td>
            <td><strong>${car.formatted_price}</strong></td>
            <td>
                <button class="btn btn-outline btn-sm" style="color:#CC0000; border-color:#CC0000;" onclick="deleteCarListing('${car._id}', '${car.brand} ${car.model}')">
                    Delete
                </button>
            </td>
        </tr>
    `).join("");
}

function renderAdminPagination(current, totalPages) {
    const pagContainer = document.getElementById("adminPagination");
    if (!pagContainer) return;

    if (totalPages <= 1) {
        pagContainer.innerHTML = "";
        return;
    }

    let html = "";
    for (let p = 1; p <= totalPages; p++) {
        html += `<button class="page-btn ${p === current ? 'active' : ''}" onclick="loadAdminInventory(${p})">${p}</button>`;
    }
    pagContainer.innerHTML = html;
}

function setupAdminTabs() {
    const tabView = document.getElementById("tabViewCars");
    const tabAdd = document.getElementById("tabAddCar");
    const contentView = document.getElementById("contentViewCars");
    const contentAdd = document.getElementById("contentAddCar");
    const searchWrapper = document.getElementById("adminSearchWrapper");

    if (tabView && tabAdd) {
        tabView.addEventListener("click", () => {
            tabView.classList.add("active");
            tabAdd.classList.remove("active");
            contentView.classList.remove("hidden");
            contentAdd.classList.add("hidden");
            if (searchWrapper) searchWrapper.classList.remove("hidden");
        });

        tabAdd.addEventListener("click", () => {
            tabAdd.classList.add("active");
            tabView.classList.remove("active");
            contentAdd.classList.remove("hidden");
            contentView.classList.add("hidden");
            if (searchWrapper) searchWrapper.classList.add("hidden");
        });
    }
}

function setupAdminSearch() {
    const searchInput = document.getElementById("adminSearchInput");
    if (searchInput) {
        let timer = null;
        searchInput.addEventListener("input", () => {
            clearTimeout(timer);
            timer = setTimeout(() => loadAdminInventory(1), 300);
        });
    }
}

function setupAdminAddCarForm() {
    const form = document.getElementById("addCarForm");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const payload = {};
        formData.forEach((val, key) => payload[key] = val);

        const btn = document.getElementById("submitAddCarBtn");
        btn.disabled = true;
        btn.innerText = "Adding Record...";

        try {
            const res = await fetch("/api/cars", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const json = await res.json();
            btn.disabled = false;
            btn.innerText = "Add Car to Database";

            if (json.success) {
                alert("Car listing added successfully to MongoDB!");
                form.reset();
                loadAdminStats();
                // Switch back to view tab
                document.getElementById("tabViewCars").click();
                loadAdminInventory(1);
            } else {
                alert(`Error: ${json.message}`);
            }
        } catch (err) {
            btn.disabled = false;
            btn.innerText = "Add Car to Database";
            alert(`Network error: ${err.message}`);
        }
    });
}

async function deleteCarListing(carId, carName) {
    if (!confirm(`Are you sure you want to delete '${carName}' from database?`)) {
        return;
    }

    try {
        const res = await fetch(`/api/cars/${carId}`, { method: "DELETE" });
        const json = await res.json();

        if (json.success) {
            loadAdminStats();
            loadAdminInventory(adminCurrentPage);
        } else {
            alert(`Error deleting record: ${json.message}`);
        }
    } catch (e) {
        alert(`Network error: ${e.message}`);
    }
}
