// Load history from localStorage or start fresh
let historyData = JSON.parse(localStorage.getItem("fakeNewsHistory") || "[]");

const inputText = document.getElementById("inputText");
const confidenceRing = document.getElementById("confidenceRing");
const confidenceValue = document.getElementById("confidenceValue");
const predictionValue = document.getElementById("predictionValue");
const summaryValue = document.getElementById("summaryValue");
const notice = document.getElementById("notice");
const predictionBanner = document.getElementById("predictionBanner");
const historyList = document.getElementById("historyList");
const clearHistoryBtn = document.getElementById("clearHistoryBtn");

function renderHistory() {
  if (!historyList) return;
  if (historyData.length === 0) {
    historyList.innerHTML =
      '<li class="history-empty">No checks yet. Enter a headline to verify.</li>';
    return;
  }

  historyList.innerHTML = historyData
    .map(
      (item, index) => `
      <li class="history-item" data-index="${index}" title="Click to reload this text">
        <span class="history-text">${escapeHtml(item.text)}</span>
        <span class="history-badge ${item.isFake ? "fake" : "real"}">
          ${item.label} (${item.confidence}%)
        </span>
      </li>
    `,
    )
    .join("");

  // Attach click listener to reload text on click
  document.querySelectorAll(".history-item").forEach((el) => {
    el.addEventListener("click", () => {
      const idx = Number(el.getAttribute("data-index"));
      if (historyData[idx]) {
        inputText.value = historyData[idx].text;
        inputText.focus();
        notice.textContent = "Loaded selected headline from history.";
      }
    });
  });
}

function escapeHtml(str) {
  return (str || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

async function verifyNews() {
  const text = inputText.value.trim();
  if (!text) {
    notice.textContent = "Please enter a headline or paragraph first.";
    inputText.focus();
    return;
  }
  notice.textContent = "Checking with the trained model...";
  try {
    const endpoint =
      window.location.origin && window.location.origin.startsWith("http")
        ? `${window.location.origin}/predict`
        : "http://127.0.0.1:8001/predict";

    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    if (!response.ok || data.error) {
      throw new Error(data.error || "Prediction request failed.");
    }

    const confidence = Math.round(Number(data.confidence) * 100);
    const isFake = data.prediction === "FAKE";
    const label = isFake ? "FAKE" : "REAL";
    const summary = isFake
      ? "The trained model found patterns associated with misleading news. Review the source and evidence."
      : "The trained model found stronger credibility signals. Continue checking the source and date.";

    confidenceValue.textContent = `${confidence}%`;
    predictionValue.textContent = `${data.prediction} · ${data.language_detected || "unknown"}`;
    predictionBanner.textContent = isFake ? "FAKE NEWS" : "REAL NEWS";
    predictionBanner.className = `prediction-banner ${isFake ? "fake" : "real"}`;
    summaryValue.textContent = summary;
    confidenceRing.style.borderColor = isFake ? "#9a6b24" : "#6b8a42";
    notice.textContent = "Prediction completed by the trained model.";

    // Save to history (keep top 15)
    historyData.unshift({
      text: text,
      label: label,
      confidence: confidence,
      isFake: isFake,
    });
    if (historyData.length > 15) historyData.pop();
    localStorage.setItem("fakeNewsHistory", JSON.stringify(historyData));
    renderHistory();
  } catch (error) {
    notice.textContent = `Model unavailable: ${error.message}`;
  }
}

// Event Listeners
document.getElementById("verifyButton").addEventListener("click", verifyNews);
document
  .getElementById("themeToggle")
  .addEventListener("click", () => document.body.classList.toggle("dark"));

if (clearHistoryBtn) {
  clearHistoryBtn.addEventListener("click", () => {
    historyData = [];
    localStorage.removeItem("fakeNewsHistory");
    renderHistory();
    notice.textContent = "History cleared.";
  });
}

document.getElementById("logoutButton").addEventListener("click", () => {
  notice.textContent = "Demo logout action selected.";
});

// Initial render
renderHistory();
