// ======================================
// Trade Trans Carrier Onboarding
// Frontend 2.0
// app.js
// ======================================
console.log("APP JS - NOWA WERSJA");


const API_URL =
    window.location.hostname === "127.0.0.1" ||
    window.location.hostname === "localhost"
        ? "${API_URL}"
        : "https://carrier-onboarding.onrender.com";

const countries = [
    { code: "PL", name: "Polska" },
    { code: "AL", name: "Albania" },
    { code: "AT", name: "Austria" },
    { code: "BE", name: "Belgia" },
    { code: "BA", name: "Bośnia i Hercegowina" },
    { code: "BG", name: "Bułgaria" },
    { code: "HR", name: "Chorwacja" },
    { code: "CY", name: "Cypr" },
    { code: "CZ", name: "Czechy" },
    { code: "DK", name: "Dania" },
    { code: "EE", name: "Estonia" },
    { code: "FI", name: "Finlandia" },
    { code: "FR", name: "Francja" },
    { code: "GR", name: "Grecja" },
    { code: "ES", name: "Hiszpania" },
    { code: "NL", name: "Holandia" },
    { code: "IE", name: "Irlandia" },
    { code: "IS", name: "Islandia" },
    { code: "LI", name: "Liechtenstein" },
    { code: "LT", name: "Litwa" },
    { code: "LU", name: "Luksemburg" },
    { code: "LV", name: "Łotwa" },
    { code: "MT", name: "Malta" },
    { code: "DE", name: "Niemcy" },
    { code: "NO", name: "Norwegia" },
    { code: "PT", name: "Portugalia" },
    { code: "RO", name: "Rumunia" },
    { code: "RS", name: "Serbia" },
    { code: "SK", name: "Słowacja" },
    { code: "SI", name: "Słowenia" },
    { code: "CH", name: "Szwajcaria" },
    { code: "SE", name: "Szwecja" },
    { code: "UA", name: "Ukraina" },
    { code: "HU", name: "Węgry" },
    { code: "GB", name: "Wielka Brytania" },
    { code: "IT", name: "Włochy" }
];

const country = document.getElementById("country");
const countryText = document.getElementById("countryText");
const countryList = document.getElementById("countryList");
const countrySearch = document.getElementById("countrySearch");

const identifier = document.getElementById("identifier");
const startButton = document.getElementById("startButton");
const buttonText = document.getElementById("buttonText");
const buttonSpinner = document.getElementById("buttonSpinner");
const statusContent = document.getElementById("statusContent");
const companyData = document.getElementById("companyData");
const companyTitle = document.getElementById("companyTitle");
const downloadedFiles = document.getElementById("downloadedFiles");
const openFolderButton = document.getElementById("openFolderButton");
const verificationAssistantButton = document.getElementById("verificationAssistantButton");
const verificationPanel = document.getElementById("verificationPanel");
const startVerificationButton = document.getElementById("startVerificationButton");
const selectedFiles = document.getElementById("selectedFiles");
const uploadBox = document.querySelector(".upload-box");
const addMoreFiles = document.getElementById("addMoreFiles");
let currentFolder = "";
let uploadedFiles = [];
const statusSection = document.getElementById("statusSection");
const statusTitle = document.getElementById("statusTitle");
const documentsTitle = document.getElementById("documentsTitle");

const detailsTab = document.getElementById("detailsTab");
const aiTab = document.getElementById("aiTab");
const chooseFilesButton =
    document.getElementById("chooseFilesButton");

const verificationFiles =
    document.getElementById("verificationFiles");

const verificationButtons =
    document.getElementById("verificationButtons");
const detailsPanel = document.getElementById("detailsPanel");
const aiPanel = document.getElementById("aiPanel");
const chooseFilesButtonBottom =
    document.getElementById("chooseFilesButtonBottom");
let selectedCountry = "";

init();

function init() {

    buildCountryList();

    bindEvents();

}

function bindEvents() {

    country.addEventListener("click", toggleCountryList);

    document.addEventListener("click", closeCountryList);

    identifier.addEventListener("input", normalizeIdentifier);

    identifier.addEventListener("blur", detectIdentifier);

    startButton.addEventListener("click", startOnboarding);

    countrySearch.addEventListener("input", filterCountries);

}
function buildCountryList() {

    const search = document.getElementById("countrySearch");

    if (!countryList.contains(search)) {

        countryList.appendChild(search);

    }

    countries.forEach(item => {

        const row = document.createElement("div");

        row.className = "country-item";

        row.innerHTML = `
            <strong>${item.code}</strong>
            <span>${item.name}</span>
        `;

        row.addEventListener("click", (e) => {

            e.stopPropagation();

            selectCountry(item);

        });

        countryList.appendChild(row);

    });

}
function toggleCountryList(e) {

    e.stopPropagation();

    countrySearch.value = "";

    filterCountries();

    countryList.classList.toggle("show");

    if (countryList.classList.contains("show")) {

        setTimeout(() => {

            countrySearch.focus();

        }, 50);

    }

}

function closeCountryList() {

    countryList.classList.remove("show");

}

function selectCountry(item) {

    selectedCountry = item.code;

    countryText.textContent = item.code;

    country.classList.remove("error");

    countryList.classList.remove("show");

}



function startOnboarding() {

    if (selectedCountry === "") {

        countryText.textContent = "Kraj";

        country.classList.add("error");

        identifier.focus();

        return;

    }

    showStatusWaiting();

}
function showStatusWaiting() {

    statusContent.innerHTML = `
        ⏳ CEIDG<br>
        ○ REGON<br>
        ○ KRS<br>
        ○ VIES
    `;

    setTimeout(() => {

        statusContent.innerHTML = `
            ✔ CEIDG<br>
            ⏳ REGON<br>
            ○ KRS<br>
            ○ VIES
        `;

    }, 1000);

    setTimeout(() => {

        statusContent.innerHTML = `
            ✔ CEIDG<br>
            ✔ REGON<br>
            ⏳ KRS<br>
            ○ VIES
        `;

    }, 2000);

    setTimeout(() => {

        statusContent.innerHTML = `
            ✔ CEIDG<br>
            ✔ REGON<br>
            ✔ KRS<br>
            ⏳ VIES
        `;

    }, 3000);

    setTimeout(() => {

        statusContent.innerHTML = `
            ✔ CEIDG<br>
            ✔ REGON<br>
            ✔ KRS<br>
            ✔ VIES
        `;

    }, 4000);

}
// ======================================
// Funkcje pomocnicze
// ======================================

function setCountry(code) {

    const found = countries.find(c => c.code === code);

    if (!found) {
        return;
    }

    selectedCountry = found.code;

    countryText.textContent = found.code;

    country.classList.remove("error");

}

function clearCountry() {

    selectedCountry = "";

    countryText.textContent = "--";

    country.classList.remove("error");

}

function getIdentifierData() {

    return {
        country: selectedCountry,
        identifier: identifier.value.trim()
    };

}

function validateForm() {

    if (selectedCountry === "") {

        countryText.textContent = "Kraj";

        country.classList.add("error");

        return false;

    }

    if (identifier.value.trim() === "") {

        identifier.focus();

        return false;

    }

    return true;

}

function resetStatus() {

    statusContent.innerHTML = '<span class="status-ready">🟢 Gotowy</span>';

}

function resetForm() {

    clearCountry();

    identifier.value = "";

    resetStatus();

}
// ======================================
// Backend (przygotowanie)
// ======================================

async function runOnboarding() {

    const data = getIdentifierData();
    statusSection.style.display = "block";
    document.getElementById("resultsPanel").style.display = "block";
    showSpinner();

    const response = await fetch(

        `${API_URL}/company-data?country=${data.country}&tax_id=${data.identifier}`

    );

     const result = await response.json();

     showCompanyData(result);

     console.log(result);

     const pdfResponse = await fetch(

          `${API_URL}/company-pdf?country=${data.country}&tax_id=${data.identifier}`

     );

     const pdfResult = await pdfResponse.json();

    console.log(pdfResult);
    showDownloadedFiles(pdfResult);
    hideSpinner();
    buttonText.textContent = "Odśwież";

}

startButton.removeEventListener("click", startOnboarding);

startButton.addEventListener("click", async () => {

    if (buttonText.textContent === "Odśwież") {

        location.reload();

        return;

    }

    if (!validateForm()) {
        return;
    }

    showStatusWaiting();

    await runOnboarding();

});
// ======================================
// Public API
// ======================================

window.App = {

    getCountry() {

        return selectedCountry;

    },

    getIdentifier() {

        return identifier.value.trim();

    },

    getData() {

        return getIdentifierData();

    },

    reset() {

        resetForm();

    },

    setStatus(html) {

        statusContent.innerHTML = html;

    }

};

// ======================================
// Start aplikacji
// ======================================

resetStatus();

console.log("Trade Trans Carrier Onboarding 2.0 uruchomiony");

function filterCountries() {

    const text = countrySearch.value.toLowerCase();

    document.querySelectorAll(".country-item").forEach(item => {

        const value = item.textContent.toLowerCase();

        if (value.includes(text)) {

            item.style.display = "flex";

        } else {

            item.style.display = "none";

        }

    });

}
function showCompanyData(data) {

    companyTitle.style.display = "block";
    companyData.style.display = "block";

    companyData.innerHTML = `

        <div class="label">Nazwa</div>
        <div class="value">${data.company_name ?? "-"}</div>

        <div class="label">Kraj</div>
        <div class="value">${data.country ?? "-"}</div>

        <div class="label">NIP</div>
        <div class="value">${data.tax_id ?? "-"}</div>

        <div class="label">REGON</div>
        <div class="value">${data.regon ?? "-"}</div>

        <div class="label">Źródło</div>
        <div class="value">${data.source ?? "-"}</div>

        <div class="label">Typ podmiotu</div>
        <div class="value">${data.entity_type ?? "-"}</div>

        <div class="label">Forma prawna</div>
        <div class="value">${data.forma_prawna ?? "-"}</div>

    `;

}
function showSpinner() {

    startButton.disabled = true;

    buttonText.textContent = "Pobieranie dokumentów...";

    buttonSpinner.classList.remove("hidden");

}

function hideSpinner() {

    startButton.disabled = false;

    buttonText.textContent = "Rozpocznij";

    buttonSpinner.classList.add("hidden");

}
function showDownloadedFiles(data) {

    if (data.pdf_path) {

        currentFolder = data.pdf_path.substring(
            0,
            data.pdf_path.lastIndexOf("\\")
        );
        console.log(currentFolder);

    }
    
    documentsTitle.style.display = "block";

    statusTitle.textContent = "";

    statusContent.style.display = "none";
    

    const files = [];

    if (data.pdf_path)
        files.push("📄 CEIDG / KRS");

    if (data.regon_pdf_path)
        files.push("📄 REGON");

    if (data.vies_pdf_path)
        files.push("📄 VIES");

    downloadedFiles.innerHTML = files.join("<br>");

    downloadedFiles.style.display = "block";

    openFolderButton.style.display = "block";

    verificationAssistantButton.style.display = "block";

    companyData.style.display = "block";

    buttonText.textContent = "Odśwież";

}
openFolderButton.addEventListener("click", async () => {

    console.log("Kliknięto przycisk");
    console.log(currentFolder);

    if (!currentFolder)
        return;

    try {

        await fetch(

            "${API_URL}/open-folder?path=" +

            encodeURIComponent(currentFolder)

        );

    }
    catch (error) {

        console.error(error);

    }

});


function normalizeIdentifier() {

    identifier.value = identifier.value.replace(/[\s\-./]/g, "");

}
function detectIdentifier() {

    country.classList.remove("error");

    let value = identifier.value.toUpperCase().trim();

    if (value === "") {
        clearCountry();
        return;
    }

    const prefix = value.substring(0, 2);

    const found = countries.find(c => c.code === prefix);

    if (found) {

        setCountry(found.code);

        value = value.substring(2);

    }
    else if (/^\d+$/.test(value)) {

        selectedCountry = "";

        countryText.textContent = "Kraj";

        country.classList.add("error");

    }
    else {

        clearCountry();

    }

    identifier.value = value.replace(/\D/g, "");

}
verificationAssistantButton.addEventListener("click", () => {

    verificationAssistantButton.style.display = "none";

    uploadBox.style.display = "block";

    verificationPanel.style.display = "block";

    verificationButtons.style.display = "none";

    selectedFiles.style.display = "none";

    

});

chooseFilesButton.addEventListener("click", () => {
    verificationFiles.click();
});

chooseFilesButtonBottom.addEventListener("click", async () => {

    if (uploadedFiles.length === 0) {
        alert("Najpierw wybierz dokumenty.");
        return;
    }

    const formData = new FormData();

    formData.append("folder", currentFolder);

    uploadedFiles.forEach(file => {
        formData.append("files", file);
    });

    try {

        const response = await fetch(
            "${API_URL}/verification/upload",
            {
                method: "POST",
                body: formData
            }
        );

        if (!response.ok) {
            throw new Error("Błąd podczas uploadu dokumentów.");
        }

        await response.json();

        alert("✅ Dokumenty zostały zapisane.");

    } catch (error) {

        console.error(error);
        alert(error.message);

    }

});
addMoreFiles.addEventListener("click", () => {

    verificationFiles.click();

});
uploadBox.addEventListener("dragover", (event) => {

    event.preventDefault();

    uploadBox.classList.add("dragover");

});

uploadBox.addEventListener("dragleave", () => {

    uploadBox.classList.remove("dragover");

});

uploadBox.addEventListener("drop", (event) => {

    event.preventDefault();

    uploadBox.classList.remove("dragover");

    verificationFiles.files = event.dataTransfer.files;

    verificationFiles.dispatchEvent(new Event("change"));

});

verificationFiles.addEventListener("change", () => {

    if (verificationFiles.files.length === 0) {
        return;
    }

    Array.from(verificationFiles.files).forEach(file => {

        const exists = uploadedFiles.some(f =>
            f.name === file.name &&
            f.size === file.size
        );

        if (!exists) {
            uploadedFiles.push(file);
        }

    });

    renderUploadedFiles();

    document.getElementById("verificationButtons").style.display = "flex";
    startVerificationButton.style.display = "block";

    verificationFiles.value = "";

});

function renderUploadedFiles() {

    uploadBox.style.display = "none";
    addMoreFiles.style.display = "block";

    selectedFiles.style.display = "block";

    let html = `<h2 class="section-title">Załączone dokumenty</h2>`;

    uploadedFiles.forEach(file => {

        html += `
            <div class="selected-file">
                📄 ${file.name}
            </div>
        `;

    });

    selectedFiles.innerHTML = html;

}

startVerificationButton.addEventListener("click", async () => {

    console.log("ANALIZUJ KLIK");

    const analyzeData = new FormData();

    analyzeData.append("folder", currentFolder);

    const aiContent = document.getElementById("ai-content");

    console.log(aiContent);

    // Przełącz na zakładkę AI
    aiTab.classList.add("active");
    detailsTab.classList.remove("active");

    aiPanel.style.display = "block";
    detailsPanel.style.display = "none";

    aiContent.innerHTML = `
        <div class="ai-loader">
            <div class="spinner"></div>
            <h3>Analizuję dokumenty...</h3>
            <p>To może potrwać około minuty.</p>
        </div>
    `;

    try {

        const analyzeResponse = await fetch(
            "${API_URL}/verification/analyze",
            {
                method: "POST",
                body: analyzeData
            }
        );

        if (!analyzeResponse.ok) {
            throw new Error("Błąd podczas analizy dokumentów.");
        }

        const analyzeResult = await analyzeResponse.json();

        aiContent.innerHTML = `
            <div class="ai-report">
                <pre>${analyzeResult.report}</pre>
            </div>
        `;

    } catch (error) {

        console.error(error);

        aiContent.innerHTML = `
            <div class="ai-error">
                ❌ Nie udało się przeprowadzić analizy dokumentów.
            </div>
        `;

        alert(error.message);
    }

});
detailsTab.addEventListener("click", () => {

    detailsTab.classList.add("active");
    aiTab.classList.remove("active");

    detailsPanel.style.display = "block";
    aiPanel.style.display = "none";

});

aiTab.addEventListener("click", () => {

    aiTab.classList.add("active");
    detailsTab.classList.remove("active");

    aiPanel.style.display = "block";
    detailsPanel.style.display = "none";

});
const aboutLink = document.getElementById("aboutLink");
const aboutModal = document.getElementById("aboutModal");
const closeAbout = document.getElementById("closeAbout");

aboutLink.addEventListener("click", (e) => {

    e.preventDefault();

    aboutModal.style.display = "flex";

});

closeAbout.addEventListener("click", () => {

    aboutModal.style.display = "none";

});

aboutModal.addEventListener("click", (e) => {

    if (e.target === aboutModal) {

        aboutModal.style.display = "none";

    }

});