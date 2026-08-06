const promptInput = document.getElementById("prompt");
const generateBtn = document.getElementById("generateBtn");
const statusText = document.getElementById("statusText");

const trayEmpty = document.getElementById("trayEmpty");
const printEl = document.getElementById("print");
const resultImage = document.getElementById("resultImage");
const scanline = document.getElementById("scanline");
const trayActions = document.getElementById("trayActions");
const downloadBtn = document.getElementById("downloadBtn");

const historyList = document.getElementById("historyList");
const historyEmpty = document.getElementById("historyEmpty");

async function loadHistory() {
  try {
    const response = await fetch("/history");
    const items = await response.json();

    if (items.length === 0) {
      historyEmpty.hidden = false;
      return;
    }

    historyEmpty.hidden = true;
    historyList.innerHTML = "";

    items.forEach((item) => {
      const div = document.createElement("div");
      div.className = "history-item";
      div.innerHTML = `
        <img src="${item.image_url}" alt="">
        <span>${item.prompt}</span>
      `;
      div.addEventListener("click", () => showImage(item.image_url));
      historyList.appendChild(div);
    });
  } catch (err) {
    console.error("Could not load history:", err);
  }
}

function showImage(url) {
  scanline.style.animation = "none";
  void scanline.offsetWidth;
  scanline.style.animation = "";

  resultImage.style.animation = "none";
  void resultImage.offsetWidth;
  resultImage.style.animation = "";

  resultImage.src = url;
  downloadBtn.href = url;

  trayEmpty.hidden = true;
  printEl.hidden = false;
  trayActions.hidden = false;
}

async function generateImage() {
  const prompt = promptInput.value.trim();

  if (!prompt) {
    statusText.textContent = "write a prompt first";
    statusText.className = "status error";
    return;
  }

  generateBtn.disabled = true;
  statusText.textContent = "developing...";
  statusText.className = "status working";

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: prompt }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Something went wrong");
    }

    showImage(data.image_url);
    promptInput.value = "";

    statusText.textContent = "ready";
    statusText.className = "status";

    loadHistory(); // refresh sidebar with the new image
  } catch (err) {
    statusText.textContent = "error: " + err.message;
    statusText.className = "status error";
  } finally {
    generateBtn.disabled = false;
  }
}

generateBtn.addEventListener("click", generateImage);

promptInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    generateImage();
  }
});

// Auto-grow the textarea as you type, like a chat input
promptInput.addEventListener("input", () => {
  promptInput.style.height = "auto";
  promptInput.style.height = promptInput.scrollHeight + "px";
});

// Load history when the page first opens
loadHistory();