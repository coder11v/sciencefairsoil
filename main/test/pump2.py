from gpiozero import DigitalOutputDevice
from time import sleep

# smart - pump1
# dumb - pump2

# active_high=False: 0V (Low) = ON, 3.3V (High) = OFF
# initial_value=False: Starts at the "OFF" state (3.3V)
pump2 = DigitalOutputDevice(27, active_high=False, initial_value=False)
pump1 = DigitalOutputDevice(17, active_high=False, initial_value=False)

def on(pumpnum, duration):
    if pumpnum == "smart":
        print("Pump 1 ON")
        pump1.on()
        sleep(duration)
        pump1.off()
        print("Pump 1 OFF")
    elif pumpnum == "dumb":
        print("Pump 2 ON")
        pump2.on()
        sleep(duration)
        pump2.off()
        print("Pump 2 OFF")
    else:
        raise ValueError(f"Invalid pump name: {pumpnum}")

try:
    on("dumb", 1)
    sleep(2)
    on("smart", 1)
finally:
    # Safety cleanup
    pump2.off()
    pump1.off()
    print("\nCleanup: All pumps set to OFF (3.3V)")