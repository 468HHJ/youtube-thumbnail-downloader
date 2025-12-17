const form = document.querySelector("form");
const fetchBtn = document.querySelector("button[type='submit']");
const loading = document.getElementById("loading");
const themeBtn = document.getElementById("themeBtn");

// Form submit - show loading
form.addEventListener("submit", () => {
    fetchBtn.innerText = "Fetching thumbnail...";
    fetchBtn.disabled = true;
    if (loading) loading.style.display = "block";
});

// Copy URL buttons
document.addEventListener("click", (e) => {
    if(e.target.classList.contains("copyBtn")) {
        const link = e.target.dataset.link;
        navigator.clipboard.writeText(link).then(() => {
            e.target.innerText = "Copied!";
            setTimeout(() => { e.target.innerText = "Copy URL"; }, 1500);
        });
    }
});

// Download button - direct download
document.addEventListener("click", (e) => {
    if(e.target.classList.contains("downloadBtn")) {
        const link = e.target.dataset.link;
        const a = document.createElement("a");
        a.href = link;
        a.download = ""; // Optional filename
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
});

// Theme toggle
if (themeBtn) {
    themeBtn.addEventListener("click", () => {
        document.body.classList.toggle("light");
        themeBtn.innerText = document.body.classList.contains("light") 
            ? "Switch to Dark Mode" 
            : "Switch to Light Mode";
    });
}
