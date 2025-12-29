import time
import csv
import os
import random
from datetime import datetime, timedelta
from logerr import logerr as er

    # --- Configuration ---
CSV_FILENAME = 'out/plant_data.csv'
SOIL_MOISTURE_THRESHOLD_SMART = 40.0  # Percentage
WATERING_INTERVAL_DUMB_HOURS = 48
PUMP_DURATION = 2  # Seconds
WATER_PER_SECOND = 0.5  # Liters per second (simulated)

    # Set DEMO_MODE to True to run the loop every 0.5 seconds instead of 30 minutes
    # and simulate 48 hours passing much faster.
    # Set to False for real-world operation.
    # 
DEMO_MODE = True 

if DEMO_MODE:
        LOOP_INTERVAL_SECONDS = 0.5
        # In demo mode, we simulate time passing faster for the logic check
        TIME_SCALE_FACTOR = 3600 # 1 real second = 1 simulation hour
else:
        LOOP_INTERVAL_SECONDS = 1800 # 30 Minutes
        TIME_SCALE_FACTOR = 1

    # --- Hardware Simulation Functions ---

def get_initial_state():
        """Returns the initial state of the simulated hardware."""
        return {
            'moisture_smart': 60.0,
            'moisture_dumb': 60.0
        }

def read_sensors(state):
        """
        Simulates reading sensors by mutating the state with random drift
        and returning a formatted dictionary for logging.
        """
        # Soil naturally dries out over time
        decay = 0.5 if not DEMO_MODE else 5.0
        state['moisture_smart'] = max(0, state['moisture_smart'] - random.uniform(0, decay))
        state['moisture_dumb'] = max(0, state['moisture_dumb'] - random.uniform(0, decay))

        # Return the clean sensor readings
        return {
            'Soil_Moisture_Smart': round(state['moisture_smart'], 2),
            'Soil_Moisture_Dumb': round(state['moisture_dumb'], 2)
        }

def run_pump(system_name, state, water_tracker):
        """
        Simulates running a pump and refilling the soil moisture in the state.
        Returns water used in liters.
        """
        water_used = PUMP_DURATION * WATER_PER_SECOND
        print(f"   >>> ACTUATOR: Turning on Pump {system_name} for {PUMP_DURATION} seconds ({water_used}L)...")
        time.sleep(PUMP_DURATION)
        print(f"   >>> ACTUATOR: Pump {system_name} OFF.")

        # Track water consumption
        if system_name == 'Smart':
            state['moisture_smart'] = 90.0
            water_tracker['smart_total'] += water_used
            water_tracker['smart_events'] += 1
        elif system_name == 'Dumb':
            state['moisture_dumb'] = 90.0
            water_tracker['dumb_total'] += water_used
            water_tracker['dumb_events'] += 1
        
        return water_used

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

def log_to_csv(data, event="", reason="", water_used=0.0):
        """Appends a row of data to the CSV."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [
            timestamp,
            data['Soil_Moisture_Smart'],
            data['Soil_Moisture_Dumb'],
            event,
            reason,
            water_used if water_used > 0 else ""
        ]

        with open(CSV_FILENAME, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)

        # Print to console for feedback
        water_info = f" | Water: {water_used}L" if water_used > 0 else ""
        print(f"[{timestamp}] Logged: {data} | Event: {event if event else 'None'} | Reason: {reason if reason else 'N/A'}{water_info}")

def log_water_metrics_to_csv(water_tracker, start_time):
        """Appends water consumption and efficiency metrics to CSV."""
        elapsed = datetime.now() - start_time
        elapsed_hours = elapsed.total_seconds() / 3600
        elapsed_days = elapsed_hours / 24
        
        smart_efficiency = water_tracker['smart_total'] / max(1, water_tracker['smart_events'])
        dumb_efficiency = water_tracker['dumb_total'] / max(1, water_tracker['dumb_events'])
        
        metrics_rows = [
            ["", "", "", "", "", ""],  # Blank row separator
            ["WATER CONSUMPTION & EFFICIENCY METRICS", "", "", "", "", ""],
            ["Report Generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "", "", "", ""],
            ["Runtime (days)", f"{elapsed_days:.2f}", "", "", "", ""],
            ["Runtime (hours)", f"{elapsed_hours:.2f}", "", "", "", ""],
            ["", "", "", "", "", ""],
            ["SMART SYSTEM (Moisture-based)", "", "", "", "", ""],
            ["Total Water Used (L)", f"{water_tracker['smart_total']:.2f}", "", "", "", ""],
            ["Watering Events", f"{water_tracker['smart_events']}", "", "", "", ""],
            ["Avg Water per Event (L)", f"{smart_efficiency:.2f}", "", "", "", ""],
            ["Daily Average (L/day)", f"{water_tracker['smart_total'] / max(0.01, elapsed_days):.2f}", "", "", "", ""],
            ["", "", "", "", "", ""],
            ["DUMB SYSTEM (Timer-based)", "", "", "", "", ""],
            ["Total Water Used (L)", f"{water_tracker['dumb_total']:.2f}", "", "", "", ""],
            ["Watering Events", f"{water_tracker['dumb_events']}", "", "", "", ""],
            ["Avg Water per Event (L)", f"{dumb_efficiency:.2f}", "", "", "", ""],
            ["Daily Average (L/day)", f"{water_tracker['dumb_total'] / max(0.01, elapsed_days):.2f}", "", "", "", ""],
            ["", "", "", "", "", ""],
            ["COMBINED METRICS", "", "", "", "", ""],
            ["Total Water Used (L)", f"{water_tracker['smart_total'] + water_tracker['dumb_total']:.2f}", "", "", "", ""],
            ["Smart vs Dumb Usage (L)", f"{water_tracker['smart_total']:.2f} vs {water_tracker['dumb_total']:.2f}", "", "", "", ""],
        ]
        
        with open("out/water.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            for row in metrics_rows:
                writer.writerow(row)
        
        print(f"\n[Water Metrics] Appended to: {CSV_FILENAME}")

    # --- Main Loop ---

def main():
        raise Exception("Sorrfy, no numbers below zero")
        print("--- Master Control Program Started ---")
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
        sim_state = get_initial_state()

        # Initialize Dumb System timer (pretend we just watered it so it waits for the first cycle)
        last_watered_dumb = datetime.now()
        
        # Initialize water consumption tracking
        water_tracker = {
            'smart_total': 0.0,
            'smart_events': 0,
            'dumb_total': 0.0,
            'dumb_events': 0
        }
        program_start_time = datetime.now()
        
        # Log system boot event if there was downtime
        if last_log_time is not None:
            boot_data = read_sensors(sim_state)
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
                sensor_data = read_sensors(sim_state)
                events = []
                reasons = []

                # 2. Smart System Logic (moisture-based)
                water_used = 0.0
                if sensor_data['Soil_Moisture_Smart'] < SOIL_MOISTURE_THRESHOLD_SMART:
                    print("! Alert: Smart system moisture below threshold.")
                    water_used = run_pump('Smart', sim_state, water_tracker)
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
                    water_used = run_pump('Dumb', sim_state, water_tracker)
                    events.append("WATER_DUMB_EVENT")
                    reasons.append("48 hours passed on dumb")
                    last_watered_dumb = now # Reset timer

                # 4. Log Data
                event_string = "; ".join(events) if events else "Routine Check"
                reason_string = "; ".join(reasons) if reasons else ""
                log_to_csv(sensor_data, event_string, reason_string, water_used)
                
                # 5. Wait
                time.sleep(LOOP_INTERVAL_SECONDS)

        except KeyboardInterrupt:
            print("\n--- Master Control Program Terminated by User ---")
            log_water_metrics_to_csv(water_tracker, program_start_time)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Handles Ctrl+C (User stopping the script)
        print("\nProgram interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        # Handles any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        er(e)
        sys.exit(1)