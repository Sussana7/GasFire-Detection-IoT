  const socket = io();
  socket.on("connect", () => {
    console.log("Connected to server via Socket.IO");
  });

  socket.on("sensor_update", (data) => {
    console.log("Live data:", data);

    // Update DOM elements
    document.getElementById("tempValue").textContent = data.temperature_c;
    document.getElementById("humidityValue").textContent = data.humidity;
    document.getElementById("gasValue").textContent = data.gas_state;
    document.getElementById("lastUpdate").textContent =
      "Last Updated: " + data.timestamp;

    // Update UI logic as before (badges, banners, etc.)
  });
 const gasBadge = document.getElementById("gasBadge");

  if (gasState == "No Gas") {
    gasBadge.className = "badge badge-safe";
    gasBadge.textContent = "Normal";
  }// else if (gasLevel < 75) {
  //   gasBadge.className = "badge badge-warning";
  //   gasBadge.textContent = "Elevated";
  // }
   else {
    gasBadge.className = "badge badge-danger";
    gasBadge.textContent = "Critical";
  }
  

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

  // checks both temp and gas
    if (gasState == "Gas Present"|| temp >= 45) {
    statusBanner.className = "status-banner status-danger";
    statusText.textContent = "Danger";
    statusDescription.textContent = "CRITICAL: Emergency protocol activated";
    statusIcon.textContent = "✕";
  } else if (gasState == "Gas Present" || temp >= 35) {
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


  const logTableBody = document.getElementById("logTableBody");
  let logData = [];  // keep history in memory

  socket.on("log_update", (entry) => {
    // Push new entry at the front
    logData.unshift(entry);

    // Keep only 10 latest
    if (logData.length > 10) {
      logData.pop();
    }

    // Rebuild table body
    logTableBody.innerHTML = "";
    logData.forEach((row, index) => {
      const tr = document.createElement("tr");

      tr.innerHTML = `
        <td>${row.timestamp}</td>
        <td>${row.temperature_c}</td>
        <td>${row.humidity}</td>
        <td>${row.gas_state}</td>
      `;

      logTableBody.appendChild(tr);
    });
  });



// Call this from the "Refresh" button
function refreshData() {
  loadIncidentTable();
}

// Auto-load on page
document.addEventListener("DOMContentLoaded", () => {
  loadIncidentTable();
});

// Helper to make headers readable
function formatHeader(header) {
  switch (header) {
    case "timestamp": return "Timestamp";
    case "temperature_c": return "Temperature (°C)";
    case "humidity": return "Humidity (%)";
    case "gas_state": return "Gas State";
    default: return header;
  }
}

// Load once on page load
document.addEventListener("DOMContentLoaded", () => {
  loadLogTable();
});






function refreshData() {
  updateSensorData();
}


// Update sensor data every 3 seconds to simulate real-time monitoring
setInterval(updateSensorData, 3000);
