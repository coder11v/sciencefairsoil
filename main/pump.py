"""
smart - pump1
dumb - plant2
"""

from gpiozero import DigitalOutputDevice
from time import sleep

# Initialize devices with Active Low logic
# active_high=False: .on() sets pin to 0V (Triggers Relay)
# active_high=False: .off() sets pin to 3.3V (Stops Relay)
pump1 = DigitalOutputDevice(17, active_high=False, initial_value=False)
pump2 = DigitalOutputDevice(27, active_high=False, initial_value=False)

def pump1_on():
    """Turns on Pump 1 while ensuring Pump 2 is locked OFF."""
    pump2.off() # Explicitly lock pump 2 High (3.3V)
    pump1.on()  # Set pump 1 Low (0V)
    print("Pump 1 is ON")

def pump1_off():
    """Turns off Pump 1."""
    pump1.off()
    print("Pump 1 is OFF")

def pump2_on():
    """Turns on Pump 2 while ensuring Pump 1 is locked OFF."""
    pump1.off() # Explicitly lock pump 1 High (3.3V)
    pump2.on()  # Set pump 2 Low (0V)
    print("Pump 2 is ON")

def pump2_off():
    """Turns off Pump 2."""
    pump2.off()
    print("Pump 2 is OFF")

# --- EXAMPLE MAIN LOOP ---
try:
    print("Starting automated system...")
    while True:
        # Example: Run pump 1 for 5 seconds
        pump1_on()
        sleep(5)
        pump1_off()

        sleep(2) # Stabilization gap

        # Example: Run pump 2 for 5 seconds
        pump2_on()
        sleep(5)
        pump2_off()

        print("Waiting for next cycle...")
        sleep(10) # Wait 10 seconds before repeating

except KeyboardInterrupt:
    print("\nStopping system...")

finally:
    # Safety cleanup: Force both High (OFF)
    pump1.off()
    pump2.off()
    print("System safe. All pumps OFF.")