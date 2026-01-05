from gpiozero import DigitalOutputDevice
from time import sleep

# dumb - pump1
# smart - pump2

# active_high=False: 0V (Low) = ON, 3.3V (High) = OFF
# initial_value=False: Starts at the "OFF" state (3.3V)
pump2 = DigitalOutputDevice(27, active_high=False, initial_value=False)
pump1 = DigitalOutputDevice(17, active_high=False, initial_value=False)

def on(pumpnum, duration):
    if pumpnum == "dumb":
        print(">>> Pump 1 ON")
        pump1.on()
        sleep(duration)
        pump1.off()
        print(">>> Pump 1 OFF")
    elif pumpnum == "smart":
        print(">>> Pump 2 ON")
        pump2.on()
        sleep(duration)
        pump2.off()
        print(">>> Pump 2 OFF")
    else:
        raise ValueError(f"Invalid pump name: {pumpnum}")
def safety():
    # Safety cleanup
    pump2.off()
    pump1.off()
    print("\n>>> Cleanup: All pumps set to OFF (3.3V)")

try:
    on("smart", 0)
    sleep(2)
    on("dumb", 5)
finally:
    safety()
    