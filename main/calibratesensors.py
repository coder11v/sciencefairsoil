#!/usr/bin/env python3
"""
SOIL MOISTURE SENSOR CALIBRATION SCRIPT
Author: Veer Bajaj
Date: 2026-01-02
REMADE: 2026-01-06

This script calibrates both capacitive soil moisture sensors in TWO states:
1. DRY soil (no water) = 0%
2. WET soil (saturated) = 100%

Collects high-precision voltage readings for accurate linear interpolation.
No files created - just outputs calibration data to console.
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
from adafruit_ads1x15.analog_in import AnalogIn

# ============================================================================
# SETUP ADC
# ============================================================================
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115.ADS1115(i2c)

# Create analog inputs for both sensors
sensor_a0 = AnalogIn(ads, 0)  # Sensor A on A0
sensor_a1 = AnalogIn(ads, 1)  # Sensor B on A1

# ============================================================================
# CONFIGURATION
# ============================================================================
SAMPLE_SIZE = 20  # Take 20 readings for high precision
DELAY_BETWEEN_SAMPLES = 0.3  # seconds

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def take_precise_reading(sensor, num_samples=SAMPLE_SIZE):
    """
    Take multiple readings and return average, min, max, and std dev.
    Higher precision readings for calibration accuracy.
    """
    readings = []
    for i in range(num_samples):
        readings.append(sensor.voltage)
        time.sleep(DELAY_BETWEEN_SAMPLES)
    
    avg_voltage = sum(readings) / len(readings)
    min_voltage = min(readings)
    max_voltage = max(readings)
    
    # Calculate standard deviation
    variance = sum((x - avg_voltage) ** 2 for x in readings) / len(readings)
    std_dev = variance ** 0.5
    
    return {
        'avg': avg_voltage,
        'min': min_voltage,
        'max': max_voltage,
        'std_dev': std_dev,
        'samples': num_samples
    }

def calibrate_one_state(state_name, sensor_a, sensor_b):
    """
    Collect high-precision calibration data for one condition.
    
    Args:
        state_name: String (e.g., "DRY" or "WET")
        sensor_a: Analog input for Sensor A
        sensor_b: Analog input for Sensor B
    
    Returns:
        Dictionary with calibration data
    """
    print(f"\n{'='*70}")
    print(f"CALIBRATION STATE: {state_name}")
    print(f"{'='*70}")
    print(f"\nInstructions:")
    
    if state_name == "DRY":
        print("1. Take Sensor A and Sensor B")
        print("2. Make sure the soil is completely DRY (no water)")
        print("3. Press ENTER when ready...")
    elif state_name == "WET":
        print("1. Water both sensors generously until soil is saturated")
        print("2. Soil should feel very wet and water may drip")
        print("3. Press ENTER when ready...")
    
    input()
    
    print(f"\n⏳ Taking {SAMPLE_SIZE} readings for each sensor...")
    print(f"   (This will take ~{SAMPLE_SIZE * DELAY_BETWEEN_SAMPLES:.0f} seconds)")
    
    reading_a = take_precise_reading(sensor_a, SAMPLE_SIZE)
    reading_b = take_precise_reading(sensor_b, SAMPLE_SIZE)
    
    print(f"\n✓ Results for {state_name}:")
    print(f"\n  Sensor A (A0):")
    print(f"    Average:    {reading_a['avg']:.6f}V")
    print(f"    Range:      {reading_a['min']:.6f}V - {reading_a['max']:.6f}V")
    print(f"    Std Dev:    {reading_a['std_dev']:.6f}V")
    
    print(f"\n  Sensor B (A1):")
    print(f"    Average:    {reading_b['avg']:.6f}V")
    print(f"    Range:      {reading_b['min']:.6f}V - {reading_b['max']:.6f}V")
    print(f"    Std Dev:    {reading_b['std_dev']:.6f}V")
    
    return {
        "state": state_name,
        "sensor_a": reading_a,
        "sensor_b": reading_b
    }

def print_calibration_summary(data_list):
    """
    Print a complete summary of calibration data with recommendations.
    """
    print(f"\n\n{'='*70}")
    print("CALIBRATION DATA SUMMARY")
    print(f"{'='*70}\n")
    
    dry_data = data_list[0]
    wet_data = data_list[1]
    
    dry_a = dry_data['sensor_a']['avg']
    wet_a = wet_data['sensor_a']['avg']
    
    dry_b = dry_data['sensor_b']['avg']
    wet_b = wet_data['sensor_b']['avg']
    
    print("SENSOR A (A0) CALIBRATION VALUES:")
    print(f"  DRY (0%):   {dry_a:.6f}V")
    print(f"  WET (100%): {wet_a:.6f}V")
    print(f"  Range:      {dry_a - wet_a:.6f}V")
    print(f"  Std Dev (DRY):  {dry_data['sensor_a']['std_dev']:.6f}V")
    print(f"  Std Dev (WET):  {wet_data['sensor_a']['std_dev']:.6f}V")
    
    print("\nSENSOR B (A1) CALIBRATION VALUES:")
    print(f"  DRY (0%):   {dry_b:.6f}V")
    print(f"  WET (100%): {wet_b:.6f}V")
    print(f"  Range:      {dry_b - wet_b:.6f}V")
    print(f"  Std Dev (DRY):  {dry_data['sensor_b']['std_dev']:.6f}V")
    print(f"  Std Dev (WET):  {wet_data['sensor_b']['std_dev']:.6f}V")
    
    print(f"\n{'='*70}")
    print("PYTHON CODE FOR sensors.py:")
    print(f"{'='*70}\n")
    
    print("# Sensor A (A0) calibration voltages")
    print(f"SENSOR_A_DRY_VOLTAGE = {dry_a:.6f}  # 0% moisture")
    print(f"SENSOR_A_WET_VOLTAGE = {wet_a:.6f}  # 100% moisture")
    
    print("\n# Sensor B (A1) calibration voltages")
    print(f"SENSOR_B_DRY_VOLTAGE = {dry_b:.6f}  # 0% moisture")
    print(f"SENSOR_B_WET_VOLTAGE = {wet_b:.6f}  # 100% moisture")
    
    print(f"\n{'='*70}\n")

# ============================================================================
# MAIN CALIBRATION FLOW
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("SMART FARM SENSOR CALIBRATION - PRECISE MODE")
    print("="*70)
    print("\nThis script will calibrate both soil moisture sensors.")
    print("High-precision readings optimized for linear interpolation.")
    print("\nWiring:")
    print("  - Sensor A on A0")
    print("  - Sensor B on A1")
    
    input("\nPress ENTER to START calibration...\n")
    
    # Collect data for DRY and WET states only
    calibration_data = []
    
    calibration_data.append(calibrate_one_state("DRY", sensor_a0, sensor_a1))
    calibration_data.append(calibrate_one_state("WET", sensor_a0, sensor_a1))
    
    # Display summary with code to copy
    print_calibration_summary(calibration_data)
    
    print("\n✓ Calibration complete!")
    print("✓ Copy the calibration values into your sensors.py file")
    print("✓ Ready to use linear interpolation with high precision!")