# main directory
## 📁 Project Structure

```text
.
├── calibratesensors.py
├── emailer.py
├── logerr.py
├── main_sim.py
├── main.py
├── out/
│   ├── archive-demo/
│   │   ├── boot_log_20251228_120030.txt
│   │   ├── boot_log_20251228_221019.txt
│   │   ├── boot_log_20251229_115959.txt
│   │   ├── errors.txt
│   │   ├── plant_data.csv
│   │   └── water.csv
│   ├── calibration_data.csv
│   ├── errors.txt
│   └── plant_data.csv
├── pump.py
├── pyproject.toml
├── README.md
├── reset.py
├── secrets/
│   ├── phone.txt
│   └── pw.txt
├── sensors.py
├── test/
│   └── pump2.py
├── testemail.py
└── uv.lock
```

---

## 🚀 Core Files (Main Logic)

### `main.py`

**Primary runtime loop.**
This is the entry point for real operation. It:

* Reads soil moisture sensors
* Applies thresholds / logic
* Activates the pump when needed
* Logs data to CSV
* Handles errors and notifications

👉 **Run this for actual deployment.**

---

### `main_sim.py`

**Simulation mode.**
Runs the same logic as `main.py` but without real hardware interaction. Useful for:

* Testing logic
* Debugging thresholds
* Development on non-hardware systems

---

## 🔧 Hardware & Sensor Modules

### `sensors.py`

Sensor abstraction layer.
Handles:

* Reading raw analog moisture values
* Converting raw readings into usable values or percentages
* Sensor-specific logic

---

### `pump.py`

Pump control logic.

* Turns the pump on/off
* Manages watering duration
* Hardware-safe isolation of pump operations

---

### `calibratesensors.py`

Sensor calibration utility.

* Records **dry**, **half-wet**, and **fully wet** states
* Writes calibration values to `out/calibration_data.csv`
* Used to normalize sensor readings into percentages

---

## 📬 Error Handling & Logging

### `logerr.py`

Centralized logging utility.

* Writes runtime errors to log files
* Prevents crashes from stopping the main loop

---

### `emailer.py`

Email notification system.

* Sends error reports and alerts
* Used for remote monitoring or failure notifications

---

### `testemail.py`

Standalone test for verifying email configuration.

---

## 📊 Output & Data Storage (`out/`)

### `out/plant_data.csv`

Primary data log.

* Timestamped soil moisture readings
* Used for analysis and visualization

---

### `out/errors.txt`

Runtime error log.

---

### `out/calibration_data.csv`

Stores sensor calibration values used by the system.

---

### `out/archive-demo/`

Archived demo data and logs.

* Old boot logs
* Historical CSV data
* Example error logs

---

## 🧪 Testing & Utilities

### `test/pump2.py`

Pump testing script.

* Used to validate pump behavior independently of the main loop

---

### `reset.py`

Utility script to reset system state.

* Useful for clearing logs or reinitializing data between runs

---

## 🔐 Secrets & Configuration

### `secrets/`

Contains sensitive data (not committed publicly):

* `phone.txt` – phone number for alerts
* `pw.txt` – email or service password

⚠️ **This directory should be excluded from version control** (`.gitignore`).

---

## 📦 Environment & Dependency Management

### `pyproject.toml`

Defines Python dependencies and project metadata.

### `uv.lock`

Lockfile for reproducible installs using `uv`.

---

## ▶️ Usage

```bash
# Run system (real hardware)
python main.py

# Run simulation
python main_sim.py

# Calibrate sensors
python calibratesensors.py
```

---

## 📝 Notes

* Designed for reliability: failures are logged and reported instead of crashing.
* Simulation mode allows full testing without sensors or pumps.
* Calibration is required before meaningful moisture percentages can be used.

---

If you want, I can also:

* Add a **Quick Start** section
* Write a **Science Fair–friendly explanation**
* Split this into **Developer vs User** documentation
* Tighten it for a GitHub public repo

Just say the word.
