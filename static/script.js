function generateReceipt() {
    const formData = new FormData(document.getElementById("receiptForm"));

    fetch("/generate", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("receiptOutput").textContent = data.receipt_text;
        document.getElementById("downloadButton").style.display = "inline-block";
    })
    .catch(error => console.error("Error:", error));
}

function downloadReceipt() {
    window.location.href = "/download";
}
