# Plant Watering System - Master Control Program

A dual-system plant watering controller that compares smart (moisture-based) vs. dumb (timer-based) watering strategies through simulation and logging.

## Features

### Current Functionality
- **Smart Watering System**: Monitors soil moisture and waters only when threshold is reached (< 40%)
- **Dumb Watering System**: Waters on a fixed 48-hour interval regardless of soil conditions
- **Sensor Simulation**: Realistic soil moisture decay with random drift
- **Comprehensive Logging**: CSV-based data logging with event tracking
- **Downtime Detection**: Automatically logs system boot events and calculates downtime
- **Demo Mode**: Accelerated simulation (1 real second = 1 simulated hour) for rapid testing

### Logging Output
- **plant_data.csv**: Timestamp, soil moisture readings (both systems), events, and reasoning
- **boot_log_*.txt**: Timestamped boot events with downtime duration

## 🚀 Future Enhancement Ideas

### Data Collection & Analysis
- [ ] **Water Consumption Tracking**: Log total water used per system and calculate efficiency metrics
- [ ] **Dry Biomass Logging**: Track plant health indicators (could be estimated from sustained low moisture events or sensor calibration)
- [ ] **Water Usage Comparison**: Calculate cumulative water waste in dumb system vs. smart system savings
- [ ] **Cost Analysis**: Estimate water cost differences between the two strategies

### System Improvements
- [ ] **Configurable Thresholds**: Command-line arguments for moisture threshold and watering interval
- [ ] **Multiple Plants**: Extend to monitor and control multiple plant zones independently
- [ ] **Weather Integration**: Adjust smart system based on rainfall forecasts
- [ ] **Soil Type Calibration**: Different decay rates based on soil composition
- [ ] **Plant-Specific Presets**: Predefined moisture profiles for common plants (cacti, ferns, tomatoes, etc.)

### Hardware & Integration
- [ ] **Real Sensor Support**: Replace simulation with actual I2C/GPIO sensor readings
- [ ] **Relay Control**: Interface with actual water pump relays
- [ ] **Dashboard**: Web UI to visualize real-time moisture levels and system performance
- [ ] **Mobile Alerts**: Push notifications when plants need attention or systems fail

### Analysis & Reporting
- [ ] **Performance Reports**: Generate PDF reports comparing smart vs. dumb efficiency
- [ ] **Historical Analysis**: Long-term trend analysis and seasonal patterns
- [ ] **Anomaly Detection**: Alert on unexpected moisture changes (possible leak or sensor failure)
- [ ] **Data Export**: Export to Excel, JSON, or other formats for external analysis

## Usage

### Quick Start
```bash
python3 main.py
```

### Configuration
Edit the configuration section at the top of the script:
```python
CSV_FILENAME = 'out/plant_data.csv'
SOIL_MOISTURE_THRESHOLD_SMART = 40.0  # Percentage
WATERING_INTERVAL_DUMB_HOURS = 48
PUMP_DURATION = 2  # Seconds
DEMO_MODE = True  # Set to False for real operation
LOOP_INTERVAL_SECONDS = 2  # In demo mode
TIME_SCALE_FACTOR = 3600  # 1 real second = 1 simulated hour
```

### Modes

**Demo Mode** (DEMO_MODE = True)
- Runs every 2 seconds
- 1 real second = 1 simulated hour
- Perfect for testing and development

**Live Mode** (DEMO_MODE = False)
- Runs every 30 minutes
- Real-time operation with actual sensors
- Suitable for production deployment

## Output Files

- `out/plant_data.csv` - Main sensor and event log
- `out/boot_log_*.txt` - System boot events with downtime duration

## System Design

### Smart System (Moisture-Based)
Responsive to actual plant needs. Waters only when soil moisture drops below 40%.

### Dumb System (Timer-Based)
Follows a fixed schedule (every 48 hours). May water unnecessarily or insufficiently depending on conditions.

### Simulation State
- Soil moisture naturally decays over time
- Decay is faster in DEMO_MODE to accelerate testing
- Watering events reset moisture to 90%

## Exit
Press `Ctrl+C` to gracefully terminate the program.

---

**Version**: 1.0  
**Status**: Active Development
