from gpiozero import DigitalOutputDevice
from time import sleep

# active_high=False means 0V = ON
# initial_value=False means it starts at 3.3V (OFF)
pump1 = DigitalOutputDevice(17, active_high=False, initial_value=False)
pump2 = DigitalOutputDevice(27, active_high=False, initial_value=False)

def run_test():
    # Force both OFF immediately
    pump1.off()
    pump2.off()
    sleep(1)
    print("Continue with 17 (smart)? (press enter to continue)")
    input()
    print("Running 17 (smart)... Locking 27 OFF")
    # We turn 27 OFF again right before turning 17 ON 
    # to ensure the pin is actively pushing 3.3V
    pump2.off() 
    pump1.on()
    sleep(1)
    pump1.off()

    sleep(1)
    print("Continue with 27 (dumb)? (press enter to continue)")
    input()

    print("Running 27 (dumb)... Locking 17 OFF")
    pump1.off()
    pump2.on()
    sleep(1)
    pump2.off()

try:
    run_test()
finally:
    pump1.off()
    pump2.off()
    print("Cleanup: Pins returned to 3.3V (Relay OFF state)")