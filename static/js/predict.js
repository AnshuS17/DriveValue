/**
 * DriveValue - Predict & Camera AI Photo Scanner JavaScript
 */

let brandModelCatalog = {};
let importanceChartInstance = null;
let webcamStream = null;

document.addEventListener("DOMContentLoaded", async () => {
    await loadBrandModelCatalog();
    setupModeSwitcher();
    setupCameraHandlers();
    setupFormHandlers();
});

function setupModeSwitcher() {
    const camBtn = document.getElementById("modeCameraBtn");
    const formBtn = document.getElementById("modeFormBtn");
    const camSec = document.getElementById("cameraSection");
    const formSec = document.getElementById("formSection");

    if (camBtn && formBtn) {
        camBtn.addEventListener("click", () => {
            camBtn.classList.add("active");
            formBtn.classList.remove("active");
            camSec.classList.remove("hidden");
            formSec.classList.add("hidden");
        });

        formBtn.addEventListener("click", () => {
            formBtn.classList.add("active");
            camBtn.classList.remove("active");
            formSec.classList.remove("hidden");
            camSec.classList.add("hidden");
            stopCameraStream();
        });
    }
}

function setupCameraHandlers() {
    const startCamBtn = document.getElementById("startCamBtn");
    const captureBtn = document.getElementById("capturePhotoBtn");
    const fileInput = document.getElementById("imageFileInput");
    const video = document.getElementById("webcamVideo");
    const placeholder = document.getElementById("cameraPlaceholder");
    const preview = document.getElementById("imagePreview");

    if (startCamBtn) {
        startCamBtn.addEventListener("click", async () => {
            try {
                if (webcamStream) {
                    stopCameraStream();
                    startCamBtn.innerText = "Start Camera";
                    captureBtn.classList.add("hidden");
                    video.classList.add("hidden");
                    placeholder.classList.remove("hidden");
                    return;
                }

                webcamStream = await navigator.mediaDevices.getUserMedia({
                    video: { facingMode: "environment", width: { ideal: 1280 }, height: { ideal: 720 } },
                    audio: false
                });

                video.srcObject = webcamStream;
                video.classList.remove("hidden");
                placeholder.classList.add("hidden");
                preview.classList.add("hidden");
                captureBtn.classList.remove("hidden");
                startCamBtn.innerText = "Stop Camera";

            } catch (err) {
                alert(`Camera Access Error: ${err.message}. Please enable camera permissions or use File Upload.`);
            }
        });
    }

    if (captureBtn) {
        captureBtn.addEventListener("click", () => {
            const canvas = document.getElementById("captureCanvas");
            if (!canvas || !video) return;

            canvas.width = video.videoWidth || 640;
            canvas.height = video.videoHeight || 480;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

            const dataUrl = canvas.toDataURL("image/jpeg", 0.85);

            // Display captured image preview
            preview.src = dataUrl;
            preview.classList.remove("hidden");
            video.classList.add("hidden");
            stopCameraStream();
            startCamBtn.innerText = "Start Camera";
            captureBtn.classList.add("hidden");

            // Process image valuation
            processCameraValuation(dataUrl);
        });
    }

    if (fileInput) {
        fileInput.addEventListener("change", (e) => {
            const file = e.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = (event) => {
                const dataUrl = event.target.result;
                preview.src = dataUrl;
                preview.classList.remove("hidden");
                video.classList.add("hidden");
                placeholder.classList.add("hidden");
                stopCameraStream();

                processCameraValuation(dataUrl);
            };
            reader.readAsDataURL(file);
        });
    }
}

function stopCameraStream() {
    if (webcamStream) {
        webcamStream.getTracks().forEach(track => track.stop());
        webcamStream = null;
    }
}

async function processCameraValuation(base64Image) {
    const overlay = document.getElementById("scannerOverlay");
    const statusText = document.getElementById("scanStatusText");
    
    if (overlay) overlay.classList.remove("hidden");

    // Scanner animation status text updates
    const statuses = [
        "AI Scanning Vehicle Silhouette...",
        "Detecting Drivetrain & Body Type...",
        "Estimating Exterior Visual Condition...",
        "Querying DriveValue ML Regression Engine..."
    ];

    let step = 0;
    const interval = setInterval(() => {
        step++;
        if (step < statuses.length && statusText) {
            statusText.innerText = statuses[step];
        }
    }, 600);

    try {
        const res = await fetch("/api/predict-image", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image: base64Image })
        });

        clearInterval(interval);
        if (overlay) overlay.classList.add("hidden");

        const json = await res.json();

        if (json.success) {
            renderResult(json);
        } else {
            alert(`Valuation Error: ${json.message}`);
        }
    } catch (err) {
        clearInterval(interval);
        if (overlay) overlay.classList.add("hidden");
        alert(`Network Error: ${err.message}`);
    }
}

async function loadBrandModelCatalog() {
    try {
        const res = await fetch("/api/brands-models");
        const json = await res.json();
        
        if (json.success && json.data) {
            brandModelCatalog = json.data;
            populateBrandDropdown();
        }
    } catch (err) {
        console.error("Failed to load brand-model catalog:", err);
    }
}

function populateBrandDropdown() {
    const brandSelect = document.getElementById("brand");
    if (!brandSelect) return;

    brandSelect.innerHTML = '<option value="">Select Brand</option>';
    const brands = Object.keys(brandModelCatalog).sort();

    brands.forEach(b => {
        const opt = document.createElement("option");
        opt.value = b;
        opt.textContent = b;
        if (b === "Toyota") opt.selected = true;
        brandSelect.appendChild(opt);
    });

    if (brandSelect.value) {
        updateModelDropdown(brandSelect.value, "Fortuner");
    }

    brandSelect.addEventListener("change", (e) => {
        updateModelDropdown(e.target.value);
    });
}

function updateModelDropdown(brandName, defaultModel = "") {
    const modelSelect = document.getElementById("model");
    if (!modelSelect) return;

    modelSelect.innerHTML = "";
    
    if (!brandName || !brandModelCatalog[brandName]) {
        modelSelect.innerHTML = '<option value="">Select Brand First</option>';
        modelSelect.disabled = true;
        return;
    }

    modelSelect.disabled = false;
    const models = brandModelCatalog[brandName];
    
    modelSelect.innerHTML = '<option value="">Select Model</option>';
    Object.keys(models).forEach(m => {
        const opt = document.createElement("option");
        opt.value = m;
        opt.textContent = m;
        if (m === defaultModel) opt.selected = true;
        modelSelect.appendChild(opt);
    });

    modelSelect.addEventListener("change", (e) => {
        const selectedModel = e.target.value;
        if (selectedModel && models[selectedModel]) {
            const spec = models[selectedModel];
            if (spec.engine) document.getElementById("engine_cc").value = spec.engine;
            if (spec.mileage) document.getElementById("mileage").value = spec.mileage;
            if (spec.seats) document.getElementById("seats").value = spec.seats;
        }
    });
}

function setupFormHandlers() {
    const form = document.getElementById("predictionForm");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        if (!validateForm()) {
            return;
        }

        const formData = new FormData(form);
        const payload = {};
        formData.forEach((val, key) => {
            payload[key] = val;
        });

        setLoadingState(true);

        try {
            const res = await fetch("/api/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const json = await res.json();
            setLoadingState(false);

            if (json.success) {
                renderResult(json);
            } else {
                alert(`Prediction Error: ${json.message || "Unable to compute price valuation."}`);
            }
        } catch (err) {
            setLoadingState(false);
            alert(`Network error: ${err.message}`);
        }
    });
}

function validateForm() {
    let isValid = true;
    document.querySelectorAll(".error-msg").forEach(el => el.innerText = "");

    const brand = document.getElementById("brand").value;
    const model = document.getElementById("model").value;
    const year = parseInt(document.getElementById("year").value);
    const kmDriven = parseInt(document.getElementById("km_driven").value);
    const engineCc = parseInt(document.getElementById("engine_cc").value);
    const mileage = parseFloat(document.getElementById("mileage").value);

    if (!brand) {
        document.getElementById("brandError").innerText = "Brand selection is required.";
        isValid = false;
    }
    if (!model) {
        document.getElementById("modelError").innerText = "Model selection is required.";
        isValid = false;
    }
    if (isNaN(year) || year < 1990 || year > 2026) {
        document.getElementById("yearError").innerText = "Valid year between 1990-2026 is required.";
        isValid = false;
    }
    if (isNaN(kmDriven) || kmDriven < 0) {
        document.getElementById("kmDrivenError").innerText = "Kilometers driven must be positive.";
        isValid = false;
    }
    if (isNaN(engineCc) || engineCc <= 0) {
        document.getElementById("engineCcError").innerText = "Engine CC must be a positive number.";
        isValid = false;
    }
    if (isNaN(mileage) || mileage <= 0) {
        document.getElementById("mileageError").innerText = "Mileage must be a positive number.";
        isValid = false;
    }

    return isValid;
}

function setLoadingState(isLoading) {
    const btn = document.getElementById("predictBtn");
    const text = document.getElementById("btnText");
    const spinner = document.getElementById("btnSpinner");

    if (isLoading) {
        btn.disabled = true;
        text.innerText = "Processing ML Model...";
        spinner.classList.remove("hidden");
    } else {
        btn.disabled = false;
        text.innerText = "Predict Car Price";
        spinner.classList.add("hidden");
    }
}

function renderResult(data) {
    const resultContainer = document.getElementById("resultContainer");
    resultContainer.classList.remove("hidden");
    resultContainer.scrollIntoView({ behavior: "smooth", block: "start" });

    document.getElementById("resaleValue").innerText = data.formatted_predicted_price;
    document.getElementById("marketRangeText").innerText = `${data.estimated_market_range.formatted_min} – ${data.estimated_market_range.formatted_max}`;
    document.getElementById("reliabilityBadge").innerText = `Model Reliability: ${data.model_reliability}`;

    const summary = data.vehicle_summary;
    document.getElementById("vehicleTitle").innerText = summary.title;
    document.getElementById("vehicleSubtitle").innerText = summary.subtitle;

    const specsContainer = document.getElementById("vehicleSpecs");
    const pills = summary.specs.split(" • ");
    specsContainer.innerHTML = pills.map(p => `<span class="spec-pill">${p}</span>`).join("");

    document.getElementById("explanationText").innerText = data.explanation;

    renderFeatureImportanceChart(data.feature_importances);
    renderSimilarCars(data.similar_cars);
}

function renderFeatureImportanceChart(importances) {
    const ctx = document.getElementById("importanceChart");
    if (!ctx) return;

    if (importanceChartInstance) {
        importanceChartInstance.destroy();
    }

    const labels = importances.map(i => i.feature);
    const values = importances.map(i => i.importance);

    importanceChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Relative Impact (%)",
                data: values,
                backgroundColor: "#111111",
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return ` Feature Weight: ${context.raw}%`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    grid: { color: "#EEEEEE" },
                    ticks: { callback: v => v + "%" }
                },
                y: {
                    grid: { display: false }
                }
            }
        }
    });
}

function renderSimilarCars(similarCars) {
    const grid = document.getElementById("similarCarsGrid");
    if (!grid) return;

    if (!similarCars || similarCars.length === 0) {
        grid.innerHTML = '<p class="text-secondary">No exact similar cars found in inventory.</p>';
        return;
    }

    grid.innerHTML = similarCars.map(car => `
        <div class="car-card">
            <div>
                <div class="car-card-header">
                    <div>
                        <div class="car-brand-model">${car.brand} ${car.model}</div>
                        <div class="car-variant">${car.variant || 'Standard'}</div>
                    </div>
                </div>
                <div class="car-specs-row">
                    ${car.year} • ${car.fuel_type} • ${car.transmission}<br>
                    ${car.km_driven.toLocaleString('en-IN')} km
                </div>
            </div>
            <div class="car-card-footer">
                <span class="car-price">${car.formatted_price}</span>
                <span class="car-location">${car.location}</span>
            </div>
        </div>
    `).join("");
}
