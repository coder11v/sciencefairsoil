# --- Python imports ---
import time
import csv
import os
import sys
import random
import traceback
from datetime import datetime, timedelta

# --- Local modules ---
from logerr import logerr as er
from emailer import send_error_email, send_water_event_msg
from sensors import get_moisture
from pump import on
from state import load_state, save_state

state = load_state()


# --- Configuration ---
CSV_FILENAME = 'out/plant_data.csv'
SOIL_MOISTURE_THRESHOLD_SMART = 40.0  # Percentage
SOIL_MOISTURE_THRESHOLD_GOAL = 70.0  # Percentage
WATERING_INTERVAL_DUMB_HOURS = 24
NUMBER_OF_POTS = 3 # Pots per group (smart/dumb)
PUMP_DURATION_SMART = 2  # Seconds
PUMP_DURATION_DUMB = 4.828571428571428  # Seconds
ML_PER_SECOND_SMART = 34.5 # mLs per second per pump
ML_PER_SECOND_DUMB = 29.5 # mLs per second per pump
ML_PER_WATER_PER_POT_SMART = (ML_PER_SECOND_SMART * PUMP_DURATION_SMART) / NUMBER_OF_POTS # mLs per pot per watering
ML_PER_WATER_PER_POT_DUMB = (ML_PER_SECOND_DUMB * PUMP_DURATION_DUMB) / NUMBER_OF_POTS # mLs per pot per watering



# Set DEMO_MODE to True to run the loop every 0.5 seconds instead of 30 minutes
# and simulate 48 hours passing much faster.
# Set to False for real-world operation.
DEMO_MODE = False

if DEMO_MODE:
        LOOP_INTERVAL_SECONDS = 0.5
        # In demo mode, we simulate time passing faster for the logic check
        TIME_SCALE_FACTOR = 3600 # 1 real second = 1 simulation hour
else:
        LOOP_INTERVAL_SECONDS = 1800 # 30 Minutes
        TIME_SCALE_FACTOR = 1

# --- Hardware Library Call Functions: Sensors ---
def read_sensors():
    """
    Returns a dictionary of sensor readings.
    """
    pct_smart = get_moisture('a0')
    pct_dumb = get_moisture('a1')

    return {
        'Soil_Moisture_Smart': pct_smart,
        'Soil_Moisture_Dumb': pct_dumb
    }

def check_smart_sensor():
        """
        Checks the smart soil moisture sensor and returns the state.
        """
        return get_moisture('a0')

def check_dumb_sensor():
        """
        Checks the dumb soil moisture sensor and returns the state.
        """
        return get_moisture('a1')

# --- Hardware Library Call Functions: Pump ---
def run_pump(system_name):
    """
    Runs a pump and refills the soil moisture.
    Returns water used in liters.
    """
    if system_name.lower() == 'smart':
        print(f"   >>> ACTUATOR: Turning on Pump {system_name} for {PUMP_DURATION_SMART} seconds...")
        on("smart", PUMP_DURATION_SMART)
        water_used_ml = (ML_PER_WATER_PER_POT_SMART * NUMBER_OF_POTS)
    elif system_name.lower() == 'dumb':
        print(f"   >>> ACTUATOR: Turning on Pump {system_name} for {PUMP_DURATION_DUMB} seconds...")
        on("dumb", PUMP_DURATION_DUMB)
        water_used_ml = (ML_PER_WATER_PER_POT_DUMB * NUMBER_OF_POTS)
    else:
        print(f"   >>> ACTUATOR: Pump {system_name} is not a valid pump name.")
        return 0
    
    print(f"   >>> ACTUATOR: Pump {system_name} OFF.")
    return water_used_ml


# --- Logging Functions ---

def initialize_csv():
        """Creates the CSV file with headers if it doesn't exist."""
        if not os.path.exists(CSV_FILENAME):
            with open(CSV_FILENAME, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Timestamp", 
                    "Soil_Moisture_Smart", 
                    "Soil_Moisture_Dumb", 
                    "Event_Log",
                    "Water_Event_Reason",
                    "Water_Used_ML"
                ])
            print(f"Created new log file: {CSV_FILENAME}")
        else:
            print(f"Log file {CSV_FILENAME} already exists. Checking for downtime...")

def get_last_log_timestamp():
        """Returns the timestamp of the last log entry, or None if CSV is empty."""
        if not os.path.exists(CSV_FILENAME):
            return None
        
        with open(CSV_FILENAME, mode='r', newline='') as file:
            lines = file.readlines()
            if len(lines) <= 1:  # Only header or empty
                return None
            
            # Get last row and extract timestamp (first column)
            last_line = lines[-1].strip()
            if not last_line:
                return None
            
            last_timestamp_str = last_line.split(',')[0]
            try:
                return datetime.strptime(last_timestamp_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return None

def create_downtime_log(downtime_hours, downtime_minutes, demo_mode=False, time_scale_factor=1):
        """Creates a downtime log file documenting the missed time."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        boot_log_filename = f"out/boot_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        simulated_hours = 0
        simulated_minutes = 0
        
        # Calculate simulated time if in demo mode
        if demo_mode:
            total_real_seconds = downtime_hours * 3600 + downtime_minutes * 60
            total_simulated_seconds = total_real_seconds * time_scale_factor
            simulated_hours = int(total_simulated_seconds // 3600)
            simulated_minutes = int((total_simulated_seconds % 3600) // 60)
        
        with open(boot_log_filename, 'w') as file:
            file.write(f"System Boot Event\n")
            file.write(f"Boot Timestamp: {timestamp}\n")
            if demo_mode:
                file.write(f"Mode: DEMO (1 real second = {int(time_scale_factor)} simulation seconds)\n")
                file.write(f"Real Downtime: {downtime_hours} hours {downtime_minutes} minutes\n")
                file.write(f"Simulated Downtime: {simulated_hours} hours {simulated_minutes} minutes\n")
            else:
                file.write(f"Mode: LIVE (real time)\n")
                file.write(f"Downtime Duration: {downtime_hours} hours {downtime_minutes} minutes\n")
        
        return boot_log_filename

def log_to_csv(data, event="", reason="", water_used_ml=0):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [
        timestamp,
        data['Soil_Moisture_Smart'],
        data['Soil_Moisture_Dumb'],
        event,
        reason,
        water_used_ml
    ]

    with open(CSV_FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)
    
    print(f"[{timestamp}] Logged: {data} | Event: {event}")

# --- Main Loop ---

def main():
    print("--- Soil Controller Started ---")
    print(f"Logging to: {CSV_FILENAME}")
    print(f"Loop Interval: {LOOP_INTERVAL_SECONDS} seconds")

    initialize_csv()

    # Check for downtime if CSV already had data
    last_log_time = get_last_log_timestamp()
    if last_log_time is not None:
        now = datetime.now()
        downtime_delta = now - last_log_time
        total_seconds = int(downtime_delta.total_seconds())
        downtime_hours = total_seconds // 3600
        downtime_minutes = (total_seconds % 3600) // 60
        
        boot_log_file = create_downtime_log(downtime_hours, downtime_minutes)
        
        print(f"! System Boot Detected: {downtime_hours} hours {downtime_minutes} minutes of downtime")
        print(f"Downtime documentation saved to: {boot_log_file}")

        # Log system boot event with current sensor data
        sensor_data = read_sensors()
        boot_reason = f"{downtime_hours} hours {downtime_minutes} minutes missed"
        log_to_csv(sensor_data, "SYSTEM_BOOT", boot_reason)

    # Initialize Dumb System timer
    if state["last_watered_dumb"]:
        last_watered_dumb = datetime.fromisoformat(state["last_watered_dumb"])
    else:
        last_watered_dumb = datetime.now()

    while True:
        # 1. Read Data
        sensor_data = read_sensors()
        events = []
        reasons = []
        water_used = 0

        # 2. Smart System Logic (moisture-based)
        if state.get("smart_system_disabled", False):
            state["smart_disabled_count"] = state.get("smart_disabled_count", 0) + 1
            print(f"! SMART SYSTEM DISABLED: Skip cycle {state['smart_disabled_count']}/1. Skipping smart watering.")
            
            if state["smart_disabled_count"] >= 1:
                print("! AUTO-RECOVERY: 1 skip cycle reached. Re-enabling smart system for next check.")
                state["smart_system_disabled"] = False
                state["smart_disabled_count"] = 0
            
            save_state(state)
            events.append("SMART_DISABLED")
            reasons.append(f"System in emergency shutdown state (Skip {state.get('smart_disabled_count', 0)}/1).")
        elif sensor_data['Soil_Moisture_Smart'] < SOIL_MOISTURE_THRESHOLD_SMART:
            print(f"Moisture low ({sensor_data['Soil_Moisture_Smart']}%). Starting deep soak...")
            # Configuration
            MAX_PUMP_CYCLES = 10
            safety = "CLEAR"  # Tracks safety status

            cycles = 0

            while sensor_data['Soil_Moisture_Smart'] < SOIL_MOISTURE_THRESHOLD_GOAL:
                if cycles >= MAX_PUMP_CYCLES:
                    safety = "TIMEOUT_EXCEEDED"
                    print("! EMERGENCY: Safety timeout reached. Check sensor.")
                    
                    # Store emergency state
                    state["smart_system_disabled"] = True
                    state["smart_disabled_count"] = 0
                    state["last_emergency_shutdown"] = datetime.now().isoformat()
                    save_state(state)
                    
                    send_error_email("Smart System Safety Timeout", "Safety timeout reached. Check sensor. System disabled until manual reset.")
                    
                    # Log emergency timeout immediately
                    cycle_water_used = run_pump('smart')
                    log_to_csv(sensor_data, "EMERGENCY_SMART_TIMEOUT", "Safety timeout reached. Check sensor.", cycle_water_used)
                    break # Stop watering immediately
        
                cycle_water_used = run_pump('smart')
                # Log each watering cycle immediately
                log_to_csv(sensor_data, "WATER_SMART_CYCLE", f"Deep soak cycle {cycles + 1}/{MAX_PUMP_CYCLES}. Moisture: {sensor_data['Soil_Moisture_Smart']}%", cycle_water_used)
                water_used += cycle_water_used
                
                time.sleep(10) # Wait for soil absorption
                cycles += 1
                sensor_data['Soil_Moisture_Smart'] = check_smart_sensor()
            
            if safety == "CLEAR":
                send_water_event_msg(pump="Smart", recipient_email="hi@veerbajaj.com")
                events.append("WATER_SMART_EVENT")
                reasons.append(f"Moisture too low on smart system. Completed {cycles} cycles.")

        # 3. Dumb System Logic (timer-based)
        now = datetime.now()
        elapsed = now - last_watered_dumb
        elapsed_hours = elapsed.total_seconds() / 3600

        if elapsed_hours >= WATERING_INTERVAL_DUMB_HOURS:
            print(f"! Timer: {WATERING_INTERVAL_DUMB_HOURS} hours passed since last Dumb system watering.")
            water_used += run_pump('dumb')
            events.append("WATER_DUMB_EVENT")
            reasons.append(f"{WATERING_INTERVAL_DUMB_HOURS} hours passed on dumb system.")
            send_water_event_msg(pump="Dumb", recipient_email="hi@veerbajaj.com")
            last_watered_dumb = now
            state["last_watered_dumb"] = now.isoformat()
            save_state(state)

        # 4. Log Data
        event_string = "; ".join(events) if events else "Routine Check"
        reason_string = "; ".join(reasons) if reasons else ""
        log_to_csv(sensor_data, event_string, reason_string, water_used)
        
        # 5. Wait
        time.sleep(LOOP_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Handles Ctrl+C (User stopping the script)
        print("\nProgram interrupted by user. Exiting...")
        send_error_email("User interrupted the soil controller", recipient_email="hi@veerbajaj.com")
        sys.exit(0)
    except Exception as e:
        
        tb = traceback.format_exc()  # ← full traceback as a string
        # Handles any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        er(e, tb)
        send_error_email(e, recipient_email="hi@veerbajaj.com")
        sys.exit(1)