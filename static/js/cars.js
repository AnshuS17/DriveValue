/**
 * DriveWorth - Used Cars Catalog JavaScript
 */

let currentPage = 1;
let currentView = "grid";
let searchDebounceTimeout = null;

document.addEventListener("DOMContentLoaded", async () => {
    await populateBrandFilter();
    setupFilterListeners();
    setupViewToggles();
    setupModalListeners();
    loadCarsCatalog(1);
});

async function populateBrandFilter() {
    const brandSelect = document.getElementById("filterBrand");
    if (!brandSelect) return;

    try {
        const res = await fetch("/api/brands-models");
        const json = await res.json();
        if (json.success && json.data) {
            const brands = Object.keys(json.data).sort();
            brands.forEach(b => {
                const opt = document.createElement("option");
                opt.value = b;
                opt.textContent = b;
                brandSelect.appendChild(opt);
            });
        }
    } catch (e) {
        console.error("Error loading brand filter options:", e);
    }
}

function setupFilterListeners() {
    const searchInput = document.getElementById("carSearch");
    const brandSelect = document.getElementById("filterBrand");
    const fuelSelect = document.getElementById("filterFuel");
    const transSelect = document.getElementById("filterTransmission");
    const yearSelect = document.getElementById("filterYear");
    const resetBtn = document.getElementById("resetFiltersBtn");

    if (searchInput) {
        searchInput.addEventListener("input", () => {
            clearTimeout(searchDebounceTimeout);
            searchDebounceTimeout = setTimeout(() => loadCarsCatalog(1), 300);
        });
    }

    [brandSelect, fuelSelect, transSelect, yearSelect].forEach(el => {
        if (el) el.addEventListener("change", () => loadCarsCatalog(1));
    });

    if (resetBtn) {
        resetBtn.addEventListener("click", () => {
            if (searchInput) searchInput.value = "";
            if (brandSelect) brandSelect.value = "";
            if (fuelSelect) fuelSelect.value = "";
            if (transSelect) transSelect.value = "";
            if (yearSelect) yearSelect.value = "";
            loadCarsCatalog(1);
        });
    }
}

function setupViewToggles() {
    const gridBtn = document.getElementById("viewGridBtn");
    const tableBtn = document.getElementById("viewTableBtn");
    const gridContainer = document.getElementById("carsGrid");
    const tableContainer = document.getElementById("tableContainer");

    if (gridBtn && tableBtn) {
        gridBtn.addEventListener("click", () => {
            currentView = "grid";
            gridBtn.classList.add("active");
            tableBtn.classList.remove("active");
            gridContainer.classList.remove("hidden");
            tableContainer.classList.add("hidden");
        });

        tableBtn.addEventListener("click", () => {
            currentView = "table";
            tableBtn.classList.add("active");
            gridBtn.classList.remove("active");
            tableContainer.classList.remove("hidden");
            gridContainer.classList.add("hidden");
        });
    }
}

async function loadCarsCatalog(page = 1) {
    currentPage = page;
    const search = document.getElementById("carSearch")?.value.trim() || "";
    const brand = document.getElementById("filterBrand")?.value || "";
    const fuel_type = document.getElementById("filterFuel")?.value || "";
    const transmission = document.getElementById("filterTransmission")?.value || "";
    const year = document.getElementById("filterYear")?.value || "";

    const params = new URLSearchParams({
        page: page,
        limit: 12,
        search: search,
        brand: brand,
        fuel_type: fuel_type,
        transmission: transmission,
        year: year
    });

    try {
        const res = await fetch(`/api/cars?${params.toString()}`);
        const json = await res.json();

        if (json.success && json.data) {
            renderCars(json.data.cars);
            renderPagination(json.data.page, json.data.pages);
            
            const resultsCount = document.getElementById("resultsCount");
            if (resultsCount) {
                resultsCount.innerText = `Showing ${json.data.cars.length} of ${json.data.total} cars`;
            }
        }
    } catch (e) {
        console.error("Error loading cars catalog:", e);
    }
}

function renderCars(cars) {
    const gridContainer = document.getElementById("carsGrid");
    const tableBody = document.getElementById("carsTableBody");
    const emptyState = document.getElementById("emptyState");

    if (!cars || cars.length === 0) {
        if (gridContainer) gridContainer.innerHTML = "";
        if (tableBody) tableBody.innerHTML = "";
        if (emptyState) emptyState.classList.remove("hidden");
        return;
    }

    if (emptyState) emptyState.classList.add("hidden");

    // Render Grid View
    if (gridContainer) {
        gridContainer.innerHTML = cars.map(car => `
            <div class="car-card" onclick="openCarModal('${car._id}')">
                <div>
                    <div class="car-card-header">
                        <div>
                            <div class="car-brand-model">${car.brand} ${car.model}</div>
                            <div class="car-variant">${car.variant || 'Standard'}</div>
                        </div>
                    </div>
                    <div class="car-specs-row">
                        ${car.year} • ${car.fuel_type} • ${car.transmission}<br>
                        ${car.km_driven.toLocaleString('en-IN')} km • ${car.ownership}
                    </div>
                </div>
                <div class="car-card-footer">
                    <span class="car-price">${car.formatted_price}</span>
                    <span class="car-location">${car.location}</span>
                </div>
            </div>
        `).join("");
    }

    // Render Table View
    if (tableBody) {
        tableBody.innerHTML = cars.map(car => `
            <tr onclick="openCarModal('${car._id}')" style="cursor:pointer;">
                <td><strong>${car.brand} ${car.model}</strong><br><small class="text-secondary">${car.variant || ''}</small></td>
                <td>${car.year}</td>
                <td>${car.fuel_type}</td>
                <td>${car.transmission}</td>
                <td>${car.km_driven.toLocaleString('en-IN')} km</td>
                <td>${car.location}</td>
                <td><strong>${car.formatted_price}</strong></td>
                <td><button class="btn btn-outline btn-sm" onclick="event.stopPropagation(); openCarModal('${car._id}')">Details</button></td>
            </tr>
        `).join("");
    }
}

function renderPagination(current, totalPages) {
    const pagContainer = document.getElementById("pagination");
    if (!pagContainer) return;

    if (totalPages <= 1) {
        pagContainer.innerHTML = "";
        return;
    }

    let html = "";
    for (let p = 1; p <= totalPages; p++) {
        html += `<button class="page-btn ${p === current ? 'active' : ''}" onclick="loadCarsCatalog(${p})">${p}</button>`;
    }
    pagContainer.innerHTML = html;
}

function setupModalListeners() {
    const modal = document.getElementById("carModal");
    const closeBtn = document.getElementById("modalClose");

    if (closeBtn) {
        closeBtn.addEventListener("click", () => {
            if (modal) modal.classList.add("hidden");
        });
    }

    if (modal) {
        modal.addEventListener("click", (e) => {
            if (e.target === modal) modal.classList.add("hidden");
        });
    }
}

async function openCarModal(carId) {
    const modal = document.getElementById("carModal");
    if (!modal) return;

    try {
        const res = await fetch(`/api/cars/${carId}`);
        const json = await res.json();
        
        if (json.success && json.data) {
            const car = json.data;

            document.getElementById("modalTitle").innerText = `${car.brand} ${car.model}`;
            document.getElementById("modalSubtitle").innerText = `${car.variant || 'Standard'} • ${car.year} • ${car.location}`;
            document.getElementById("modalPrice").innerText = car.formatted_price;

            const specsGrid = document.getElementById("modalSpecsGrid");
            specsGrid.innerHTML = `
                <div class="modal-spec-item"><strong>Fuel:</strong> ${car.fuel_type}</div>
                <div class="modal-spec-item"><strong>Transmission:</strong> ${car.transmission}</div>
                <div class="modal-spec-item"><strong>KM Driven:</strong> ${car.km_driven.toLocaleString('en-IN')} km</div>
                <div class="modal-spec-item"><strong>Engine CC:</strong> ${car.engine_cc} CC</div>
                <div class="modal-spec-item"><strong>Mileage:</strong> ${car.mileage} kmpl</div>
                <div class="modal-spec-item"><strong>Ownership:</strong> ${car.ownership}</div>
                <div class="modal-spec-item"><strong>Condition:</strong> ${car.condition}</div>
                <div class="modal-spec-item"><strong>Insurance:</strong> ${car.insurance_valid ? 'Valid' : 'Expired'}</div>
            `;

            modal.classList.remove("hidden");

            // Calculate estimated market value using predict API
            const estPriceEl = document.getElementById("modalEstPrice");
            estPriceEl.innerText = "Estimating ML Valuation...";

            fetch("/api/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(car)
            }).then(r => r.json()).then(pResult => {
                if (pResult.success) {
                    estPriceEl.innerText = pResult.formatted_predicted_price;
                } else {
                    estPriceEl.innerText = "N/A";
                }
            }).catch(() => {
                estPriceEl.innerText = "N/A";
            });
        }
    } catch (e) {
        console.error("Error fetching car details:", e);
    }
}
