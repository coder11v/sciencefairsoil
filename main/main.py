import time
import csv
import os
import sys
import random
import traceback
from datetime import datetime, timedelta
from logerr import logerr as er
from emailer import send_error_email, send_water_event_msg
from sensors import get_moisture
from pump import on

    # --- Configuration ---
CSV_FILENAME = 'out/plant_data.csv'
SOIL_MOISTURE_THRESHOLD_SMART = 30.0  # Percentage TODO
SOIL_MOISTURE_THRESHOLD_GOAL = 80.0  # Percentage TODO
WATERING_INTERVAL_DUMB_HOURS = 24
PUMP_DURATION_SMART = 2  # Seconds, TODO
PUMP_DURATION_DUMB = 2  # Seconds, TODO


    # Set DEMO_MODE to True to run the loop every 0.5 seconds instead of 30 minutes
    # and simulate 48 hours passing much faster.
    # Set to False for real-world operation.
    # 
DEMO_MODE = True # TODO

if DEMO_MODE:
        LOOP_INTERVAL_SECONDS = 0.5
        # In demo mode, we simulate time passing faster for the logic check
        TIME_SCALE_FACTOR = 3600 # 1 real second = 1 simulation hour
else:
        LOOP_INTERVAL_SECONDS = 1800 # 30 Minutes
        TIME_SCALE_FACTOR = 1

# --- Hardware Library Call Functions: Sensors ---
def read_sensors(state=None):
    """
    Returns a dictionary of sensor readings.
    """
    pct_smart = get_moisture('a0')
    pct_dumb = get_moisture('a1')

    return state, {
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
        """
        if system_name == 'Smart':
                print(f"   >>> ACTUATOR: Turning on Pump {system_name} for {PUMP_DURATION_SMART} seconds...")
                on("smart", PUMP_DURATION_SMART)
        elif system_name == 'Dumb':
                print(f"   >>> ACTUATOR: Turning on Pump {system_name} for {PUMP_DURATION_DUMB} seconds...")
                on("dumb", PUMP_DURATION_DUMB)
        print(f"   >>> ACTUATOR: Pump {system_name} OFF.")


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
                    "Water_Used_L"
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

def log_to_csv(data, event="", reason=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [
        timestamp,
        data['Soil_Moisture_Smart'],
        data['Soil_Moisture_Dumb'],
        event,
        reason
    ]

    with open(CSV_FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)
    
    print(f"[{timestamp}] Logged: {data} | Event: {event}")

# --- Main Loop ---

def main():
        print("--- Soil Controller Started ---")
        print(f"Mode: {'DEMO' if DEMO_MODE else 'LIVE'}")
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
            
            boot_log_file = create_downtime_log(downtime_hours, downtime_minutes, DEMO_MODE, TIME_SCALE_FACTOR)
            
            # Calculate simulated time for console output
            if DEMO_MODE:
                total_real_seconds = downtime_hours * 3600 + downtime_minutes * 60
                total_simulated_seconds = total_real_seconds * TIME_SCALE_FACTOR
                sim_hours = int(total_simulated_seconds // 3600)
                sim_minutes = int((total_simulated_seconds % 3600) // 60)
                print(f"! System Boot Detected: {downtime_hours}h {downtime_minutes}m real time ({sim_hours}h {sim_minutes}m simulated)")
            else:
                print(f"! System Boot Detected: {downtime_hours} hours {downtime_minutes} minutes of downtime")
            print(f"Downtime documentation saved to: {boot_log_file}")

        # Initialize simulation state (dictionary instead of class instance)
        sim_state = None

        # Initialize Dumb System timer (pretend we just watered it so it waits for the first cycle)
        last_watered_dumb = datetime.now()
        
       
        program_start_time = datetime.now()
        
        # Log system boot event if there was downtime
        if last_log_time is not None:
            read_sensors(sim_state)
            downtime_delta = datetime.now() - last_log_time
            total_seconds = int(downtime_delta.total_seconds())
            downtime_hours = total_seconds // 3600
            downtime_minutes = (total_seconds % 3600) // 60
            
            # Use simulated time in boot reason if demo mode is on
            if DEMO_MODE:
                total_real_seconds = downtime_hours * 3600 + downtime_minutes * 60
                total_simulated_seconds = total_real_seconds * TIME_SCALE_FACTOR
                sim_hours = int(total_simulated_seconds // 3600)
                sim_minutes = int((total_simulated_seconds % 3600) // 60)
                boot_reason = f"{sim_hours}h {sim_minutes}m simulated (demo mode)"
            else:
                boot_reason = f"{downtime_hours} hours {downtime_minutes} minutes missed"
            
            log_to_csv(boot_data, "SYSTEM_BOOT", boot_reason)

        try:
            while True:
                # 1. Read Data (passes state to modify it)
                read_sensors(sim_state)
                events = []
                reasons = []

                # 2. Smart System Logic (moisture-based)
                if sensor_data['Soil_Moisture_Smart'] < SOIL_MOISTURE_THRESHOLD_SMART:
                    print("! Alert: Smart system moisture below threshold.")
                    run_pump('smart', sim_state)
                    send_water_event_msg(pump="Smart", recipient_email="hi@veerbajaj.com")
                    events.append("WATER_SMART_EVENT")
                    reasons.append("moisture too low on smart")

                # 3. Dumb System Logic (timer-based)
                # Calculate time elapsed. In Demo mode, we fake the elapsed time.
                now = datetime.now()
                elapsed = now - last_watered_dumb

                # Logic to handle the threshold check
                effective_elapsed_hours = (elapsed.total_seconds() * TIME_SCALE_FACTOR) / 3600

                if effective_elapsed_hours > WATERING_INTERVAL_DUMB_HOURS:
                    print(f"! Timer: {WATERING_INTERVAL_DUMB_HOURS} hours passed since last Dumb system watering.")
                    run_pump('dumb', sim_state)
                    events.append("WATER_DUMB_EVENT")
                    reasons.append("48 hours passed on dumb")
                    send_water_event_msg(pump="Dumb", recipient_email="hi@veerbajaj.com")
                    last_watered_dumb = now # Reset timer

                # 4. Log Data
                event_string = "; ".join(events) if events else "Routine Check"
                reason_string = "; ".join(reasons) if reasons else ""
                log_to_csv(sensor_data, event_string, reason_string)
                
                # 5. Wait
                time.sleep(LOOP_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            print("\n--- Soil Controller Terminated by User ---")

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