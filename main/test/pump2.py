from gpiozero import DigitalOutputDevice
from time import sleep

# active_high=False: 0V (Low) = ON, 3.3V (High) = OFF
# initial_value=False: Starts at the "OFF" state (3.3V)
pump1 = DigitalOutputDevice(17, active_high=False, initial_value=False)
pump2 = DigitalOutputDevice(27, active_high=False, initial_value=False)

def run_test():
    # Ensure everything is OFF to start
    pump1.off()
    pump2.off()
    
    print("Pump 1 ON")
    pump1.on()
    sleep(1)
    pump1.off()
    print("Pump 1 OFF")
    
    sleep(2) # Short buffer for relay mechanics

    # --- PUMP 2 TEST ---
    print("\nPress Enter to trigger Pump 2 (27) for 1 second...")
    input()
    
    print("Pump 2 ON")
    pump2.on()
    sleep(1)
    pump2.off()
    print("Pump 2 OFF")

try:
    run_test()
finally:
    # Safety cleanup
    pump1.off()
    pump2.off()
    print("\nCleanup: All pumps set to OFF (3.3V)")