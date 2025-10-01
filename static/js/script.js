async function updateSensorData() {
  try {
    const response = await fetch("/api/live");
    const data = await response.json();

    if (data.error) {
      console.error(data.error);
      return;
    }

    const gasState = data.gas_state;
    const temp = parseFloat(data.temperature_c);
    const humidity = parseFloat(data.humidity);

    // Update DOM
    document.getElementById("tempValue").textContent = temp;
    document.getElementById("tempProgress").style.width = (temp / 60) * 100 + "%";
    document.getElementById("humidityValue").textContent = humidity;
    document.getElementById("gasValue").textContent = gasState;

    document.getElementById("lastUpdate").textContent =
      "Last Updated: " + data.timestamp;
        // Update gas badge
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


  } catch (err) {
    console.error("Failed to fetch sensor data:", err);
  }
  
}

// Poll every 3 seconds
setInterval(updateSensorData, 3000);


// Load incident table from backend
async function loadIncidentTable() {
  try {
    const response = await fetch("/api/log");
    const data = await response.json();

    if (!Array.isArray(data)) {
      console.error("Invalid incident data format:", data);
      return;
    }

    const tbody = document.getElementById("incidentTableBody");
    tbody.innerHTML = ""; 

    data.forEach((incident, index) => {
      const row = document.createElement("tr");

      // ID
      const idCell = document.createElement("td");
      idCell.textContent = `#${incident.id || index + 1}`;
      row.appendChild(idCell);


      // Timestamp
      const timeCell = document.createElement("td");
      timeCell.textContent = incident.timestamp;
      row.appendChild(timeCell);

      // // Description
      const descCell = document.createElement("td");
      descCell.textContent = incident.description;
      row.appendChild(descCell);


      tbody.appendChild(row);
    });
  } catch (err) {
    console.error("Failed to load incident table:", err);
  }
}



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
