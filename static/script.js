// ================= SEARCH FUNCTION =================
function search() {
    let input = document.getElementById("search").value.toLowerCase();

    let cards = document.querySelectorAll(
        ".airdrop-card, .wallet-card, .card"
    );

    cards.forEach(card => {
        let text = card.innerText.toLowerCase();

        if (text.includes(input)) {
            card.style.display = "";
        } else {
            card.style.display = "none";
        }
    });
}

// ================= COPY ADDRESS =================
function copyText(text) {
    navigator.clipboard.writeText(text)
        .then(() => {
            console.log("Copied:", text);
        })
        .catch(err => {
            console.log("Error:", err);
        });
}

// COLOR SWITCH
function setTheme(color) {
    document.body.className = color;
    localStorage.setItem("theme", color);
}

// LOAD THEME
window.onload = () => {
    let theme = localStorage.getItem("theme") || "green";
    document.body.className = theme;
};