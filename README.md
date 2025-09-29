# Smart Gas Leakage & Fire Safety System

A **Python-based IoT safety system** built with **Raspberry Pi** that detects **gas leaks** and **high temperatures**, triggers alarms, sends notifications, logs incidents into a database, and displays **real-time data** on a web dashboard built with **Flask, HTML, and CSS**.

---

## 4-Day Project Plan

---

### ✅ Day 1 – Hardware Setup & Testing + Basic Dashboard

**Goal:** Wire and test all components individually and build a simple Flask dashboard with dummy data.

#### Tasks

**Hardware Setup & Testing**
- Gather components:
  - MQ-2 gas sensor – Detects LPG/methane and other gases  
  - DHT22 sensor – Measures temperature and humidity  
  - Buzzer or speaker – Sounds alarm  
  - LEDs (red, green, blue) – Visual indicators  
  - Resistors, jumper wires, breadboard  
  - Raspberry Pi – Central controller  
- Wire and test each component individually:
  - MQ-2 → basic Python script → print gas concentration  
  - DHT22 → `Adafruit_DHT` → print temperature & humidity  
  - Buzzer & LEDs → toggle with simple script  
- Document safe and danger thresholds for gas and temperature.

**Basic Flask Dashboard (Dummy Data)**
- Set up a basic Flask project: `app.py`, `templates/`, `static/css/`
- Create `dashboard.html` with sections:
  - Current gas level  
  - Current temperature  
  - System status (Safe / Warning / Danger)  
  - Incident history (placeholder data)  
- Style with CSS for a clean, user-friendly UI.
- Render dummy sensor data through Flask.

**End-of-day target:**  
All hardware components should be tested and a basic Flask dashboard running with placeholder data.

---

### ✅ Day 2 – Sensor Integration + Real-Time Data

**Goal:** Connect sensors to Flask backend and display **live readings** on the dashboard.

#### Tasks

**Sensor Integration**
- Write Python scripts to read from MQ-2 and DHT22 sensors continuously.
- Define safe and danger thresholds for gas and temperature.
- Combine sensor readings into one script that returns a JSON response.

**Backend Integration**
- Create Flask routes to fetch real-time sensor data (e.g., `/api/sensor`).
- Use AJAX or Fetch API in the frontend to update dashboard values automatically.

**Dashboard Update**
- Replace dummy data with real sensor readings.
- Display system status dynamically based on thresholds.
- Add color-coded alerts (e.g., green = safe, yellow = warning, red = danger).

**End-of-day target:**  
Dashboard should now display **live sensor readings** and **update in real time** without needing a page refresh.

---

### ✅ Day 3 – Alerts + Database Logging

**Goal:** Implement alarms, SMS/email alerts, and database logging for incident tracking.

#### Tasks

**Alarm System**
- Write Python functions to activate buzzer and LEDs when thresholds are exceeded.
- Create different visual/audio patterns for warning vs. danger levels.

**Notifications**
- Integrate **Twilio API** to send SMS alerts when gas or temperature exceeds safe levels.
- (Optional) Set up email alerts using SMTP.

**Database Integration**
- Set up an **SQLite database**.
- Create a table for incident logs with fields like timestamp, gas level, temperature, and status.
- Modify sensor script to insert data into the database whenever a warning/danger event occurs.

**Dashboard Enhancements**
- Add a table to display incident history from the database.
- Include filters (e.g., show last 10 events, show only danger events).

**End-of-day target:**  
System should **trigger alarms**, **send alerts**, and **log incidents** automatically.

---

### ✅ Day 4 – Final Dashboard + Testing & Documentation

**Goal:** Polish the user interface, test the entire system thoroughly, and prepare final documentation.

#### Tasks

**Dashboard Finalization**
- Improve UI with better styling and layout.
- Add charts (e.g., gas level and temperature over time) using **Matplotlib** or **Chart.js**.
- Display system uptime and last alert time.

**System Testing**
- Simulate gas leaks and high temperature conditions.
- Verify:
  - Sensor readings update in real time  
  - Alarms and LEDs respond correctly  
  - SMS/email alerts are sent  
  - Database logs all incidents  

**Documentation**
- Write a clear README describing setup, components, and usage.
- Document safe/danger thresholds and how they were determined.
- Capture screenshots of dashboard and sample alerts.

**End-of-day target:**  
A fully functional, well-documented **Smart Gas & Fire Safety System** ready for presentation or deployment.

---
