// // Simulate sensor data updates
// function updateSensorData() {
//   // Random gas level between 20-80
//   const gasLevel = Math.floor(Math.random() * 60) + 20;
//   document.getElementById("gasValue").textContent = gasLevel;
//   document.getElementById("gasProgress").style.width = gasLevel + "%";

//   // Update gas badge
//   const gasBadge = document.getElementById("gasBadge");
//   if (gasLevel < 50) {
//     gasBadge.className = "badge badge-safe";
//     gasBadge.textContent = "Normal";
//   } else if (gasLevel < 75) {
//     gasBadge.className = "badge badge-warning";
//     gasBadge.textContent = "Elevated";
//   } else {
//     gasBadge.className = "badge badge-danger";
//     gasBadge.textContent = "Critical";
//   }

//   // Random temperature between 22-40
//   const temp = (Math.random() * 18 + 22).toFixed(1);
//   document.getElementById("tempValue").textContent = temp;
//   document.getElementById("tempProgress").style.width = (temp / 60) * 100 + "%";

//   // Update temp badge
//   const tempBadge = document.getElementById("tempBadge");
//   if (temp < 35) {
//     tempBadge.className = "badge badge-safe";
//     tempBadge.textContent = "Normal";
//   } else if (temp < 45) {
//     tempBadge.className = "badge badge-warning";
//     tempBadge.textContent = "Elevated";
//   } else {
//     tempBadge.className = "badge badge-danger";
//     tempBadge.textContent = "Critical";
//   }

//   // Update system status
//   const statusBanner = document.getElementById("statusBanner");
//   const statusText = document.getElementById("statusText");
//   const statusDescription = document.getElementById("statusDescription");
//   const statusIcon = statusBanner.querySelector(".status-icon");

//   if (gasLevel >= 75 || temp >= 45) {
//     statusBanner.className = "status-banner status-danger";
//     statusText.textContent = "Danger";
//     statusDescription.textContent = "CRITICAL: Emergency protocol activated";
//     statusIcon.textContent = "✕";
//   } else if (gasLevel >= 50 || temp >= 35) {
//     statusBanner.className = "status-banner status-warning";
//     statusText.textContent = "Warning";
//     statusDescription.textContent =
//       "Attention required - elevated readings detected";
//     statusIcon.textContent = "⚠";
//   } else {
//     statusBanner.className = "status-banner status-safe";
//     statusText.textContent = "Safe";
//     statusDescription.textContent = "All systems operating normally";
//     statusIcon.textContent = "✓";
//   }

//   // Update timestamp
//   const now = new Date();
//   document.getElementById("lastUpdate").textContent =
//     "Last Updated: " + now.toISOString().slice(0, 19).replace("T", " ");
// }

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



// Fetch log data and build table
// async function loadLogTable() {
//   try {
//     const response = await fetch("/api/log");
//     const logData = await response.json();

//     if (!Array.isArray(logData)) {
//       console.error("Unexpected log data format", logData);
//       return;
//     }

//     // Create table
//     const table = document.createElement("table");
//     table.className = "sensor-log-table";

//     // Create headers
//     const headers = ["timestamp", "temperature_c", "humidity", "gas_state"];
//     const headerRow = table.insertRow();
//     headers.forEach(header => {
//       const th = document.createElement("th");
//       th.textContent = formatHeader(header);
//       headerRow.appendChild(th);
//     });

//     // Fill rows
//     logData.forEach(entry => {
//       const row = table.insertRow();
//       headers.forEach(header => {
//         const cell = row.insertCell();
//         cell.textContent = entry[header];
//       });
//     });

//     // Insert table into the DOM
//     const container = document.getElementById("logTableContainer");
//     container.innerHTML = ""; // Clear previous content
//     container.appendChild(table);

//   } catch (err) {
//     console.error("Failed to load log table:", err);
//   }
// }

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
    tbody.innerHTML = ""; // Clear existing

    data.forEach((incident, index) => {
      const row = document.createElement("tr");

      // ID
      const idCell = document.createElement("td");
      idCell.textContent = `#${incident.id || index + 1}`;
      row.appendChild(idCell);

      // // Type
      // const typeCell = document.createElement("td");
      // typeCell.innerHTML = `<span class="incident-type">${incident.type}</span>`;
      // row.appendChild(typeCell);


      // Timestamp
      const timeCell = document.createElement("td");
      timeCell.textContent = incident.timestamp;
      row.appendChild(timeCell);

      // // Description
      // const descCell = document.createElement("td");
      // descCell.textContent = incident.description;
      // row.appendChild(descCell);

      // // Status
      // const statusCell = document.createElement("td");
      // statusCell.innerHTML = `<span class="status-resolved">✓ ${incident.status}</span>`;
      // row.appendChild(statusCell);

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
