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
    document.getElementById("humidityValue").textContent = humidity;
    document.getElementById("gasState").textContent = gasState;


    document.getElementById("lastUpdate").textContent =
      "Last Updated: " + data.timestamp;

  } catch (err) {
    console.error("Failed to fetch sensor data:", err);
  }
}

// Poll every 3 seconds
setInterval(updateSensorData, 3000);

