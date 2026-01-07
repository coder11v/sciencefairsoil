#!/usr/bin/env python3
"""
SENSORS.PY - Soil Moisture Sensor Library
Generated automatically from calibration data
Date: 2026-01-02T21:19:32.334305

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
    100% = Saturated/fully wet soil (low voltage)
"""

import board
import busio
import adafruit_ads1x15.ads1115 as ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

# ============================================================================
# CALIBRATION VALUES (two-point calibration)
# ============================================================================

# Sensor A (A0) calibration voltages
SENSOR_A_DRY_VOLTAGE = 2.73      # 0% moisture
SENSOR_A_WET_VOLTAGE = 1.3958     # 100% moisture

# Sensor B (A1) calibration voltages
SENSOR_B_DRY_VOLTAGE = 2.6755     # 0% moisture
SENSOR_B_WET_VOLTAGE = 1.3515     # 100% moisture

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
        >>> print(f"Soil moisture: {moisture:.1f}%")
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
        raise ValueError(f'Invalid channel: {channel}. Use "a0" or "a1"')
    
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
        raise ValueError(f'Invalid channel: {channel}. Use "a0" or "a1"')


def get_moisture_both():
    """
    Read both sensors at once.
    
    Returns:
        tuple: (moisture_a0_percent, moisture_a1_percent)
    
    Example:
        >>> a, b = get_moisture_both()
        >>> print(f"A: {a:.1f}%  B: {b:.1f}%")
        A: 45.3%  B: 52.1%
    """
    return (get_moisture("a0"), get_moisture("a1"))


if __name__ == "__main__":
    # Test the sensor readings
    print("Testing sensor readings...")
    print(f"Sensor A (A0): {get_moisture('a0'):.1f}%")
    print(f"Sensor B (A1): {get_moisture('a1'):.1f}%")
    a, b = get_moisture_both()
    print(f"Both: A={a:.1f}%  B={b:.1f}%")