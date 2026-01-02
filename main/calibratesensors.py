#!/usr/bin/env python3
"""
SOIL MOISTURE SENSOR CALIBRATION SCRIPT
Author: Veer Bajaj
Date: 2026-01-02

This script calibrates both capacitive soil moisture sensors in three states:
1. DRY soil (no water) = 0%
2. HALF WET soil (moderate moisture) = 50%
3. FULLY WET soil (saturated) = 100%

The calibration data is used to CREATE sensors.py - a reusable library
that converts raw voltage readings into percentage moisture (0-100%).

EXPORTS: sensors.py
  - get_moisture(channel) -> returns % moisture (0-100%)
  - Usage in your main script:
      from sensors import get_moisture
      moisture_a = get_moisture("a0")
      if moisture_a < 25:
          activate_pump_a()
"""

"""
to run in terminal:
sudo pip3 install adafruit-circuitpython-ads1x15
sudo pip3 install adafruit-circuitpython-busdevice
sudo pip3 install adafruit-circuitpython-register

"""

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS1115
import adafruit_ads1x15.ads1x15 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import csv
from datetime import datetime

# ============================================================================
# SETUP ADC
# ============================================================================
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115.ADS1115(i2c)

# Create analog inputs for both sensors
sensor_a0 = AnalogIn(ads, 0)  # Sensor 1 on A0 new
sensor_a1 = AnalogIn(ads, 1)  # Sensor 2 on A1 new

# ============================================================================
# CONFIGURATION
# ============================================================================
CALIBRATION_FILE = "out/calibration_data.csv"
SENSORS_PY_FILE = "sensors.py"
SAMPLE_SIZE = 10  # Take 10 readings for each state, then average
DELAY_BETWEEN_SAMPLES = 0.5  # seconds

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def take_average_reading(sensor, num_samples=SAMPLE_SIZE):
    """
    Take multiple readings and return the average voltage.
    This smooths out noise.
    """
    readings = []
    for i in range(num_samples):
        readings.append(sensor.voltage)
        time.sleep(DELAY_BETWEEN_SAMPLES)
    
    avg_voltage = sum(readings) / len(readings)
    return avg_voltage

def calibrate_one_state(state_name, sensor_a, sensor_b):
    """
    Collect calibration data for one condition (dry, half-wet, or wet).
    
    Args:
        state_name: String (e.g., "DRY", "HALF_WET", "WET")
        sensor_a: Analog input for Sensor A
        sensor_b: Analog input for Sensor B
    
    Returns:
        Dictionary with calibration data
    """
    print(f"\n{'='*60}")
    print(f"CALIBRATION STATE: {state_name}")
    print(f"{'='*60}")
    print(f"\nInstructions:")
    
    if state_name == "DRY":
        print("1. Take Sensor A (attached to pot A3)")
        print("2. Make sure the soil is completely DRY (no water)")
        print("3. Place Sensor B in a DRY pot or container")
        print("4. Press ENTER when ready...")
    elif state_name == "HALF_WET":
        print("1. Water both pots until soil is damp (not soaked)")
        print("2. Soil should feel moist to touch but not dripping")
        print("3. Press ENTER when ready...")
    elif state_name == "WET":
        print("1. Water both pots generously until soil is saturated")
        print("2. Soil should feel very wet and water may drip")
        print("3. Press ENTER when ready...")
    
    input()  # Wait for user
    
    print(f"\n✓ Taking {SAMPLE_SIZE} readings for each sensor...")
    print(f"  (This will take ~{SAMPLE_SIZE * DELAY_BETWEEN_SAMPLES} seconds)")
    
    voltage_a = take_average_reading(sensor_a, SAMPLE_SIZE)
    voltage_b = take_average_reading(sensor_b, SAMPLE_SIZE)
    
    print(f"\n✓ Results for {state_name}:")
    print(f"  Sensor A voltage: {voltage_a:.2f}V")
    print(f"  Sensor B voltage: {voltage_b:.2f}V")
    
    return {
        "state": state_name,
        "sensor_a_voltage": voltage_a,
        "sensor_b_voltage": voltage_b,
        "timestamp": datetime.now().isoformat()
    }

def save_calibration_data(data_list, filename=CALIBRATION_FILE):
    """
    Save calibration data to a CSV file for documentation.
    """
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["state", "sensor_a_voltage", "sensor_b_voltage", "timestamp"])
        writer.writeheader()
        writer.writerows(data_list)
    
    print(f"\n✓ Calibration data saved to {filename}")

def generate_sensors_py(data_list):
    """
    Generate the sensors.py library file with calibration data baked in.
    
    This creates a reusable module that converts voltage readings to percentage moisture.
    """
    # Extract voltages from calibration data
    dry_data = data_list[0]  # 0% moisture
    half_data = data_list[1]  # 50% moisture
    wet_data = data_list[2]   # 100% moisture
    
    dry_a = dry_data['sensor_a_voltage']
    half_a = half_data['sensor_a_voltage']
    wet_a = wet_data['sensor_a_voltage']
    
    dry_b = dry_data['sensor_b_voltage']
    half_b = half_data['sensor_b_voltage']
    wet_b = wet_data['sensor_b_voltage']
    
    # Generate Python file content
    python_code = f'''#!/usr/bin/env python3
"""
SENSORS.PY - Soil Moisture Sensor Library
Generated automatically from calibration data
Date: {datetime.now().isoformat()}

This module provides a simple function to read soil moisture as a percentage (0-100%).

Usage in your main script:
    from sensors import get_moisture
    
    # In your main loop:
    moisture_a = get_moisture("a0")  # Returns 0-100%
    moisture_b = get_moisture("a1")  # Returns 0-100%
    
    if moisture_a < 25:  # If less than 25% moisture
        activate_pump_a()

The percentage scale:
    0% = Completely dry soil (high voltage)
    50% = Moderately moist soil (medium voltage)
    100% = Saturated/fully wet soil (low voltage)
"""

import board
import busio
import adafruit_ads1x15.ads1115 as ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

# ============================================================================
# CALIBRATION VALUES (auto-generated from calibration script)
# ============================================================================

# Sensor A (A0) calibration voltages
SENSOR_A_DRY_VOLTAGE = {dry_a:.4f}      # 0% moisture
SENSOR_A_HALF_VOLTAGE = {half_a:.4f}    # 50% moisture
SENSOR_A_WET_VOLTAGE = {wet_a:.4f}      # 100% moisture

# Sensor B (A1) calibration voltages
SENSOR_B_DRY_VOLTAGE = {dry_b:.4f}      # 0% moisture
SENSOR_B_HALF_VOLTAGE = {half_b:.4f}    # 50% moisture
SENSOR_B_WET_VOLTAGE = {wet_b:.4f}      # 100% moisture

# ============================================================================
# ADC SETUP
# ============================================================================

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115.ADS1115(i2c)

# Create analog input channels
_channel_a0 = AnalogIn(ads, 0)
_channel_a1 = AnalogIn(ads, 1)

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def get_moisture(channel):
    """
    Read soil moisture as a percentage (0-100%).
    
    Args:
        channel (str): "a0" or "a1" (which sensor to read)
    
    Returns:
        float: Moisture percentage (0-100%)
               0% = completely dry
               100% = completely saturated
    
    Example:
        >>> moisture = get_moisture("a0")
        >>> print(f"Soil moisture: {{moisture:.1f}}%")
        Soil moisture: 45.3%
    """
    
    channel = channel.lower().strip()
    
    if channel == "a0":
        voltage = _channel_a0.voltage
        dry_v = SENSOR_A_DRY_VOLTAGE
        wet_v = SENSOR_A_WET_VOLTAGE
    elif channel == "a1":
        voltage = _channel_a1.voltage
        dry_v = SENSOR_B_DRY_VOLTAGE
        wet_v = SENSOR_B_WET_VOLTAGE
    else:
        raise ValueError(f'Invalid channel: {{channel}}. Use "a0" or "a1"')
    
    # Convert voltage to percentage
    # DRY soil = HIGH voltage (0%)
    # WET soil = LOW voltage (100%)
    # Linear interpolation between dry and wet voltages
    
    if voltage >= dry_v:
        # Voltage is higher than dry calibration (very dry)
        percentage = 0.0
    elif voltage <= wet_v:
        # Voltage is lower than wet calibration (very wet)
        percentage = 100.0
    else:
        # Linear interpolation between dry and wet
        voltage_range = dry_v - wet_v
        voltage_difference = dry_v - voltage
        percentage = (voltage_difference / voltage_range) * 100.0
    
    return percentage


def get_moisture_raw(channel):
    """
    Read raw voltage from soil moisture sensor.
    Useful for debugging or logging.
    
    Args:
        channel (str): "a0" or "a1"
    
    Returns:
        float: Raw voltage reading (in volts)
    """
    channel = channel.lower().strip()
    
    if channel == "a0":
        return _channel_a0.voltage
    elif channel == "a1":
        return _channel_a1.voltage
    else:
        raise ValueError(f'Invalid channel: {{channel}}. Use "a0" or "a1"')


def get_moisture_both():
    """
    Read both sensors at once.
    
    Returns:
        tuple: (moisture_a0_percent, moisture_a1_percent)
    
    Example:
        >>> a, b = get_moisture_both()
        >>> print(f"A: {{a:.1f}}%  B: {{b:.1f}}%")
        A: 45.3%  B: 52.1%
    """
    return (get_moisture("a0"), get_moisture("a1"))


if __name__ == "__main__":
    # Test the sensor readings
    print("Testing sensor readings...")
    print(f"Sensor A (A0): {{get_moisture('a0'):.1f}}%")
    print(f"Sensor B (A1): {{get_moisture('a1'):.1f}}%")
    a, b = get_moisture_both()
    print(f"Both: A={{a:.1f}}%  B={{b:.1f}}%")
'''
    
    # Write the sensors.py file
    with open(SENSORS_PY_FILE, 'w') as f:
        f.write(python_code)
    
    print(f"\n✓ Sensor library created: {SENSORS_PY_FILE}")
    print(f"\n  You can now use it in your main script:")
    print(f"    from sensors import get_moisture")
    print(f"    moisture_a = get_moisture('a0')  # Returns 0-100%")

def print_calibration_summary(data_list):
    """
    Print a nice summary of the calibration and interpretation.
    """
    print(f"\n{'='*60}")
    print("CALIBRATION SUMMARY")
    print(f"{'='*60}\n")
    
    print("Sensor A (A0):")
    for item in data_list:
        print(f"  {item['state']:10s}: {item['sensor_a_voltage']:.2f}V")
    
    print("\nSensor B (A1):")
    for item in data_list:
        print(f"  {item['state']:10s}: {item['sensor_b_voltage']:.2f}V")
    
    print(f"\n{'='*60}")
    print("INTERPRETATION & PERCENTAGE SCALE:")
    print(f"{'='*60}")
    
    dry_a = data_list[0]['sensor_a_voltage']
    half_a = data_list[1]['sensor_a_voltage']
    wet_a = data_list[2]['sensor_a_voltage']
    
    dry_b = data_list[0]['sensor_b_voltage']
    half_b = data_list[1]['sensor_b_voltage']
    wet_b = data_list[2]['sensor_b_voltage']
    
    print("\nSENSOR A (A0) - System A (Smart watering):")
    print(f"  {dry_a:.2f}V = 0%   (completely dry)")
    print(f"  {half_a:.2f}V = 50%  (moderately moist)")
    print(f"  {wet_a:.2f}V = 100% (fully saturated)")
    print(f"\n  ✓ THRESHOLD for watering: 25%")
    print(f"    → Pump A activates when soil falls BELOW 25% moisture")
    print(f"    → This corresponds to voltage: ~{(dry_a + half_a) / 2:.2f}V")
    
    print("\nSENSOR B (A1) - System B (Timer watering, data logging only):")
    print(f"  {dry_b:.2f}V = 0%   (completely dry)")
    print(f"  {half_b:.2f}V = 50%  (moderately moist)")
    print(f"  {wet_b:.2f}V = 100% (fully saturated)")
    
    print("\n" + "="*60)
    print("GENERATED sensors.py LIBRARY")
    print("="*60)
    print(f"\nA new file '{SENSORS_PY_FILE}' has been created with your")
    print("calibration values baked in.")
    print(f"\nUsage in your main loop:")
    print(f"  from sensors import get_moisture")
    print(f"  moisture_a = get_moisture('a0')  # Returns 0-100%")
    print(f"  if moisture_a < 25:")
    print(f"      activate_pump_a()")
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print(f"1. ✓ Review calibration_data.csv")
    print(f"2. ✓ Copy {SENSORS_PY_FILE} to your project directory")
    print(f"3. ✓ Import in your main script: from sensors import get_moisture")
    print(f"4. ✓ Use in your watering logic")
    print("\n" + "="*60 + "\n")

# ============================================================================
# MAIN CALIBRATION FLOW
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("SMART FARM SENSOR CALIBRATION")
    print("="*60)
    print("\nThis script will calibrate both soil moisture sensors.")
    print("You will be asked to place sensors in DRY, HALF-WET, and WET conditions.")
    print("\nMake sure your wiring matches the Wiring guide:")
    print("  - Sensor A (A0) in pot A3")
    print("  - Sensor B (A1) in a separate test pot")
    
    input("\nPress ENTER to START calibration...\n")
    
    # Collect data for three states
    calibration_data = []
    
    calibration_data.append(calibrate_one_state("DRY", sensor_a0, sensor_a1))
    calibration_data.append(calibrate_one_state("HALF_WET", sensor_a0, sensor_a1))
    calibration_data.append(calibrate_one_state("WET", sensor_a0, sensor_a1))
    
    # Save calibration data
    save_calibration_data(calibration_data)
    
    # Generate sensors.py library
    generate_sensors_py(calibration_data)
    
    # Display summary
    print_calibration_summary(calibration_data)
    
    print("\n✓ Calibration complete!")
    print(f"✓ Files created: {CALIBRATION_FILE}, {SENSORS_PY_FILE}")
    print("✓ Ready to start your main experiment loop!")
