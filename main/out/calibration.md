vib@thecookie:~/Soil/main $ python calibratesensors.py 

======================================================================
SMART FARM SENSOR CALIBRATION - PRECISE MODE
======================================================================

This script will calibrate both soil moisture sensors.
High-precision readings optimized for linear interpolation.

Wiring:
  - Sensor A on A0
  - Sensor B on A1

Press ENTER to START calibration...


======================================================================
CALIBRATION STATE: DRY
======================================================================

Instructions:
1. Take Sensor A and Sensor B
2. Make sure the soil is completely DRY (no water)
3. Press ENTER when ready...


⏳ Taking 20 readings for each sensor...
   (This will take ~6 seconds)

✓ Results for DRY:

  Sensor A (A0):
    Average:    2.808481V
    Range:      2.808250V - 2.808750V
    Std Dev:    0.000154V

  Sensor B (A1):
    Average:    2.812081V
    Range:      2.811875V - 2.812375V
    Std Dev:    0.000133V

======================================================================
CALIBRATION STATE: WET
======================================================================

Instructions:
1. Water both sensors generously until soil is saturated
2. Soil should feel very wet and water may drip
3. Press ENTER when ready...


⏳ Taking 20 readings for each sensor...
   (This will take ~6 seconds)

✓ Results for WET:

  Sensor A (A0):
    Average:    1.354456V
    Range:      1.354000V - 1.355125V
    Std Dev:    0.000363V

  Sensor B (A1):
    Average:    1.334206V
    Range:      1.333750V - 1.334500V
    Std Dev:    0.000195V


======================================================================
CALIBRATION DATA SUMMARY
======================================================================

SENSOR A (A0) CALIBRATION VALUES:
  DRY (0%):   2.808481V
  WET (100%): 1.354456V
  Range:      1.454025V
  Std Dev (DRY):  0.000154V
  Std Dev (WET):  0.000363V

SENSOR B (A1) CALIBRATION VALUES:
  DRY (0%):   2.812081V
  WET (100%): 1.334206V
  Range:      1.477875V
  Std Dev (DRY):  0.000133V
  Std Dev (WET):  0.000195V

======================================================================
PYTHON CODE FOR sensors.py:
======================================================================

# Sensor A (A0) calibration voltages
SENSOR_A_DRY_VOLTAGE = 2.808481  # 0% moisture
SENSOR_A_WET_VOLTAGE = 1.354456  # 100% moisture

# Sensor B (A1) calibration voltages
SENSOR_B_DRY_VOLTAGE = 2.812081  # 0% moisture
SENSOR_B_WET_VOLTAGE = 1.334206  # 100% moisture

======================================================================


✓ Calibration complete!
✓ Copy the calibration values into your sensors.py file
✓ Ready to use linear interpolation with high precision!