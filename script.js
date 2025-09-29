// Simulate sensor data updates
function updateSensorData() {
  // Random gas level between 20-80
  const gasLevel = Math.floor(Math.random() * 60) + 20;
  document.getElementById("gasValue").textContent = gasLevel;
  document.getElementById("gasProgress").style.width = gasLevel + "%";

  // Update gas badge
  const gasBadge = document.getElementById("gasBadge");
  if (gasLevel < 50) {
    gasBadge.className = "badge badge-safe";
    gasBadge.textContent = "Normal";
  } else if (gasLevel < 75) {
    gasBadge.className = "badge badge-warning";
    gasBadge.textContent = "Elevated";
  } else {
    gasBadge.className = "badge badge-danger";
    gasBadge.textContent = "Critical";
  }

  // Random temperature between 22-40
  const temp = (Math.random() * 18 + 22).toFixed(1);
  document.getElementById("tempValue").textContent = temp;
  document.getElementById("tempProgress").style.width = (temp / 60) * 100 + "%";

  // Update temp badge
  const tempBadge = document.getElementById("tempBadge");
  if (temp < 35) {
    tempBadge.className = "badge badge-safe";
    tempBadge.textContent = "Normal";
  } else if (temp < 45) {
    tempBadge.className = "badge badge-warning";
    tempBadge.textContent = "Elevated";
  } else {
    tempBadge.className = "badge badge-danger";
    tempBadge.textContent = "Critical";
  }

  // Update system status
  const statusBanner = document.getElementById("statusBanner");
  const statusText = document.getElementById("statusText");
  const statusDescription = document.getElementById("statusDescription");
  const statusIcon = statusBanner.querySelector(".status-icon");

  if (gasLevel >= 75 || temp >= 45) {
    statusBanner.className = "status-banner status-danger";
    statusText.textContent = "Danger";
    statusDescription.textContent = "CRITICAL: Emergency protocol activated";
    statusIcon.textContent = "✕";
  } else if (gasLevel >= 50 || temp >= 35) {
    statusBanner.className = "status-banner status-warning";
    statusText.textContent = "Warning";
    statusDescription.textContent =
      "Attention required - elevated readings detected";
    statusIcon.textContent = "⚠";
  } else {
    statusBanner.className = "status-banner status-safe";
    statusText.textContent = "Safe";
    statusDescription.textContent = "All systems operating normally";
    statusIcon.textContent = "✓";
  }

  // Update timestamp
  const now = new Date();
  document.getElementById("lastUpdate").textContent =
    "Last Updated: " + now.toISOString().slice(0, 19).replace("T", " ");
}

function refreshData() {
  updateSensorData();
}

// Update sensor data every 3 seconds to simulate real-time monitoring
setInterval(updateSensorData, 3000);
