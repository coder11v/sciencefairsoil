# Smart Farm Wiring Guide - Simple Version

## What You're Building

You have:
- 2 soil moisture sensors
- 1 ADC converter (reads the sensors)
- 2 water pumps
- 2 relay switches (control the pumps)
- A Raspberry Pi (the brain)

## The Basic Idea

Everything connects to the Raspberry Pi using wires and a breadboard. Think of it like:
- **Power wires** (red) = sending electricity
- **Ground wires** (black) = returning electricity
- **Data wires** = Pi talking to sensors

---

## Step 1: Power and Ground First

These go to EVERY component.

**From Raspberry Pi:**
- Take a red wire from Pin 1 (3.3V) to the breadboard's red rail
- Take a black wire from Pin 6 (Ground) to the breadboard's black rail

**This powers:**
- The soil sensors
- The ADC converter
- The temperature sensor (BME280, optional)

For the relay switches, use Pin 2 (5V) instead.

---

## Step 2: Connect the Soil Sensors

You have 2 soil sensors. Each one has 3 wires:
- Red wire = power (goes to breadboard red rail)
- Black wire = ground (goes to breadboard black rail)
- Yellow wire = signal (carries the moisture data)

**Sensor 1:**
- Red → breadboard red rail
- Black → breadboard black rail
- Yellow → ADC converter pin labeled A0

**Sensor 2:**
- Red → breadboard red rail
- Black → breadboard black rail
- Yellow → ADC converter pin labeled A1

---

## Step 3: Connect the ADC Converter

The ADC reads analog signals (moisture) and converts them to digital (numbers the Pi understands).

**Power and Ground:**
- ADC red wire → breadboard red rail
- ADC black wire → breadboard black rail

**Data Connection (these two wires are important):**
- ADC SDA pin → Raspberry Pi Pin 3 (GPIO 2)
- ADC SCL pin → Raspberry Pi Pin 5 (GPIO 3)

These are "I2C" wires - they let the Pi ask the ADC "what's the moisture level?"

---

## Step 4: Connect the Relay Switches

Relays are like remote-controlled switches. They protect the Pi by switching the pumps on/off without the Pi having to handle all that power.

**Relay 1 (controls Pump 1):**
- VCC (power) → Raspberry Pi Pin 2 (5V)
- GND (ground) → Raspberry Pi Pin 6
- IN1 (control signal) → Raspberry Pi Pin 11 (GPIO 17)

**Relay 2 (controls Pump 2):**
- VCC (power) → Raspberry Pi Pin 2 (5V)
- GND (ground) → Raspberry Pi Pin 6
- IN2 (control signal) → Raspberry Pi Pin 13 (GPIO 27)

---

## Step 5: Connect the Water Pumps

**Pump 1:**
- Red wire → 5V power (or Raspberry Pi Pin 2)
- Black wire → The relay switch (Relay 1's "COM" or middle terminal)
- Ground completes the circuit back through the relay

**Pump 2:**
- Red wire → 5V power (or Raspberry Pi Pin 2)
- Black wire → The relay switch (Relay 2's "COM" or middle terminal)
- Ground completes the circuit back through the relay

When you tell the relay to turn on, it switches the pump on. When you turn it off, the pump stops.

---

## Raspberry Pi Pin Reference

These are the pins you actually use:

```
Pin 1  = 3.3V (power for sensors)
Pin 2  = 5V (power for relays)
Pin 3  = GPIO 2 (data from ADC - SDA)
Pin 5  = GPIO 3 (data from ADC - SCL)
Pin 6  = Ground (everything returns here)
Pin 11 = GPIO 17 (controls Relay 1)
Pin 13 = GPIO 27 (controls Relay 2)
```

---

## Simple Wiring Checklist

- [ ] Red wire from Pi Pin 1 to breadboard red rail
- [ ] Black wire from Pi Pin 6 to breadboard black rail
- [ ] Both soil sensors connected (red to red rail, black to black rail)
- [ ] Sensor 1 yellow wire to ADC A0
- [ ] Sensor 2 yellow wire to ADC A1
- [ ] ADC powered (red to red rail, black to black rail)
- [ ] ADC SDA wire to Pi Pin 3
- [ ] ADC SCL wire to Pi Pin 5
- [ ] Relay 1 VCC to Pi Pin 2 (5V)
- [ ] Relay 1 GND to Pi Pin 6
- [ ] Relay 1 IN1 to Pi Pin 11
- [ ] Relay 2 VCC to Pi Pin 2 (5V)
- [ ] Relay 2 GND to Pi Pin 6
- [ ] Relay 2 IN2 to Pi Pin 13
- [ ] Pump 1 red wire to 5V
- [ ] Pump 1 black wire to Relay 1
- [ ] Pump 2 red wire to 5V
- [ ] Pump 2 black wire to Relay 2

---

## Testing Your Wiring

Before you start the experiment:

**Test 1: Check I2C connection**
```
i2cdetect -y 1
```
You should see "48" - that's your ADC converter.

**Test 2: Test Relay 1**
```python
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.HIGH)  # Relay clicks on, pump should run
GPIO.output(17, GPIO.LOW)   # Relay clicks off, pump stops
```

**Test 3: Test Relay 2**
Same as above but use pin 27 instead of 17.

---

## Common Mistakes

- **Using 5V for sensors** - They want 3.3V only. Use Pin 1, not Pin 2.
- **Forgetting ground wires** - Every component needs a ground connection.
- **Connecting pump directly to GPIO** - Always use a relay. The relay protects the Pi.
- **Wrong pins for SDA/SCL** - Pin 3 is SDA, Pin 5 is SCL. Don't mix them up.

---

## That's It

Once everything is wired and tested, your Pi can:
1. Read moisture from both sensors (via ADC)
2. Decide when to water based on moisture levels
3. Control pumps using relays

You're ready to start the experiment!