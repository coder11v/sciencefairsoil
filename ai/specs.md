# Smart Farm Project - Component Specifications

## The Stuff You're Actually Buying

Here's what each component does and what to look for when ordering.

---

## 1. Breadboard

**What to get:** Standard 400-hole solderless breadboard

**Why:** No soldering needed. Just push wires in and out.

**Specs:**
- Size: ~4 inches × 2 inches
- 400 holes (rows and columns)
- Has a red rail (positive) and black rail (ground) on each side
- Cost: $5-10

**Where to find it:**
- Amazon: search "breadboard 400 hole"
- Any electronics store
- Usually comes with jumper wires already

---

## 2. Capacitive Soil Moisture Sensors (You need 2)

**What to get:** Capacitive soil moisture sensor (NOT resistive - they rust and break)

**Why:** Capacitive sensors don't rust, last longer, and are more accurate

**Key specs:**
- Operating voltage: 3.3V to 5.5V (Raspberry Pi likes 3.3V)
- Output: Analog signal (0-3V range)
- Current draw: About 5mA (very small)
- 3 wires: Red (power), Black (ground), Yellow (signal)
- Size: About 10cm long stick that goes in the soil
- Waterproof area at the bottom
- Costs: $7-10 each (2 sensors = $15 total)

**What the reading means:**
- Dry soil: High voltage (around 2.5V)
- Wet soil: Low voltage (around 1.0V)
- The Pi reads this voltage through the ADS1115

**Where to find it:**
- Amazon: search "capacitive soil moisture sensor"
- Look for: DFRobot, AIDEEPEN, or generic "gravity interface"
- Make sure it says "capacitive" not "resistive"

---

## 3. ADS1115 ADC (Analog-to-Digital Converter) - 1 module

**What to get:** ADS1115 I2C ADC Module

**Why:** Raspberry Pi can't read analog signals directly. This translates analog (continuous voltage) into digital (numbers)

**Key specs:**
- Input voltage: 3.3V to 5V (breadboard-compatible)
- 4 channels (A0, A1, A2, A3) - you use 2
- I2C communication (only 2 wires needed: SDA + SCL)
- I2C address: 0x48 (when ADDR pin is tied to ground)
- Accuracy: 16-bit (very precise)
- Typical price: $5-8

**What it does:**
- Reads the analog voltage from each soil sensor
- Converts it to a number (0-32767)
- Sends that number to the Pi via I2C

**Where to find it:**
- Amazon: search "ADS1115 I2C ADC module"
- Comes with or without headers already soldered
- Should have 4 pins: VDD, GND, SDA, SCL
- Plus 4 input channels (A0, A1, A2, A3)

---

## 4. Water Pumps (You need 2)

**What to get:** 5V DC mini water pump (submersible or inline)

**Why:** Pumps water from a container to your plants via tubes

**Key specs:**
- Voltage: 5V DC (not AC)
- Current: 100-300mA (uses more power than sensors)
- Flow rate: 100-200 mL/min (typical)
- Two wires: Red (positive), Black (negative/ground)
- Small and quiet
- Cost: $7-10 each (2 pumps = $15 total)

**Types:**
- Submersible: Sits in water container (common, reliable)
- Inline: Water flows through it (more compact)
- For this project: submersible is easier

**Where to find it:**
- Amazon: search "5V mini water pump" or "5V submersible pump"
- Aquarium pump sections also have these
- Make sure it says 5V (not 12V or 24V)

---

## 5. Relay Modules (You need 2, or 1 dual relay)

**What to get:** 2-channel 5V relay module (controls both pumps)

**OR:** 2 individual 1-channel 5V relay modules

**Why:** Pumps need too much power for the Pi's GPIO pins. Relays are "switches" that protect the Pi

**Key specs:**
- Module voltage: 5V
- Channel count: 2 (controls 2 pumps)
- Input control: 3.3V compatible (Pi GPIO works)
- NO contact (Normally Open - pump off by default)
- COM terminal (connects to pump)
- Cost: $5-8 per channel

**How it works:**
- When Pi sends voltage to IN1 → relay 1 clicks on → pump 1 runs
- When Pi stops → relay clicks off → pump stops
- Pump never connects directly to Pi (safe)

**Pins on a 2-channel relay:**
- VCC (5V power)
- GND (ground)
- IN1 (signal from GPIO 17)
- IN2 (signal from GPIO 27)
- NO/COM terminals (connect pump power here)

**Where to find it:**
- Amazon: search "2 channel 5V relay module"
- Should say "low level triggered" (means 3.3V from Pi works)
- Comes with or without headers

---

## 6. Jumper Wires & Breadboard Connectors

**What to get:** Mixed pack of jumper wires

**Why:** Connects everything together without soldering

**Types:**
- Male-to-male: both ends have pins (most common, for breadboard)
- Female-to-female: both ends have holes (if components have pins)
- Male-to-female: one pin, one hole (adapters)

**What you need:**
- Lots of male-to-male (30+ wires)
- Colors: red (power), black (ground), other colors (signals)
- Cost: $5-10 for a big mixed pack

**Where to find it:**
- Amazon: search "jumper wire kit" or "breadboard jumper wires"
- Usually come in packs of 65-120 wires

---

## 7. Vinyl Tubing & Splitters

**What to get:** 
- Vinyl tubing: 6mm outer diameter (fits pump output)
- 5-way splitters: for dripping water to 5 plants

**Why:** Delivers water from pump to individual pots

**Specs:**
- Tubing diameter: 6mm OD × 4mm ID (outer × inner)
- Splitter: 5-way drip splitter
- Tubing length: Need 10-15 feet total (depends on setup)
- Cost: $8 total for tubing + splitters

**Where to find it:**
- Amazon: search "vinyl tubing 6mm" and "drip splitter"
- Aquarium supply stores
- Gardening sections of hardware stores
- Might also need small end caps or plugs

---

## 8. Pots & Potting Soil

**What to get:**
- 10 small pots (4-5 inches diameter)
- Potting soil (good quality, not garden soil)

**Why:** Growing medium for basil

**Specs:**
- Pot size: 4-5" diameter (big enough for basil, not too heavy to move)
- Material: Plastic or ceramic (drain hole required)
- Soil: "Indoor potting mix" or "seed starting mix"
- Drainage: Every pot needs a hole in the bottom
- Cost: $8-12 total ($5-8 soil, $3-4 pots)

**Where to find it:**
- Home Depot, Lowe's, local garden center
- Target/Walmart garden sections
- Amazon: "potting soil" and "plant pots"
- Make sure: soil says "potting mix" (not garden soil), pots have drain holes

---

## 9. Starter Plants

**What to get:** 10 basil seedlings or seeds

**Why:** Basil grows fast (2 weeks), cheap, tasty

**Options:**
- Seedlings (already sprouted) - faster, ~$1-2 each
- Seeds (plant yourself) - cheaper, takes 1-2 weeks to sprout
- For your timeline: seedlings are better

**Where to find it:**
- Local garden center (best)
- Home Depot/Lowes (seasonal)
- Amazon: "basil seedlings"
- Local nurseries
- Cost: $1-2 each (10 plants = $10-20, use ~10)

**Why basil:**
- Grows in 2 weeks
- Doesn't need perfect conditions
- You can eat it when done
- Creates good biomass for weighing

---

## 10. Digital Scale

**What to get:** Kitchen scale or precision scale, 1-2kg capacity

**Why:** Measure final plant weight (biomass) to compare systems A vs B

**Specs:**
- Capacity: 1000-2000g (enough for several plants)
- Accuracy: ±1g (kitchen scale is fine)
- Digital readout (not analog dial)
- Cost: $15-30

**Where to find it:**
- Amazon: search "digital kitchen scale"
- Target, Walmart, kitchen stores
- Any grocery/cooking section

---

## Summary: What You're Actually Ordering

| Item | Qty | Price | Where |
|------|-----|-------|-------|
| Breadboard (400 hole) | 1 | $7 | Amazon/Electronics |
| Capacitive soil sensor | 2 | $8 | Amazon |
| ADS1115 ADC module | 1 | $6 | Amazon |
| 5V water pump | 2 | $15 | Amazon/Aquarium |
| 2-channel relay module | 1 | $8 | Amazon |
| Jumper wire pack | 1 | $8 | Amazon |
| Vinyl tubing + splitter | 1 | $8 | Amazon/Garden |
| Basil seedlings | 10 | $10 | Local garden center |
| Pots + potting soil | 1 set | $10 | Home Depot/Garden |
| Digital scale | 1 | $20 | Amazon/Target |
| **TOTAL** | | **~$100** | |

---

## Pro Tips for Ordering

1. **Bundle on Amazon** - You can find "Arduino starter kits" with breadboard, jumpers, LEDs, etc. Buy those + add the specific sensors

2. **Check seller ratings** - For sensors especially, read reviews. Some cheap clones don't work well

3. **Order cables/connectors extras** - You'll lose or break jumper wires. Get 30+ to be safe

4. **Basil timing** - Seedlings mature fast (order 1 week before experiment start)

5. **Water container** - You'll need plastic containers to hold water. Use tupperware or milk jugs (not listed above but free)

---

## Double-Check List Before You Buy

- [ ] Breadboard? (400 hole, solderless)
- [ ] 2 capacitive soil sensors? (NOT resistive)
- [ ] ADS1115 module? (I2C, 4 channels)
- [ ] 2 pumps? (5V DC, NOT 12V)
- [ ] Relay module? (2 channel, 5V, 3.3V compatible)
- [ ] Jumper wires? (male-to-male pack, 60+)
- [ ] Vinyl tubing + splitters? (6mm diameter)
- [ ] 10 basil seedlings/seeds?
- [ ] Pots with drainage? (4-5" diameter)
- [ ] Potting soil? (indoor mix, not garden soil)
- [ ] Digital scale? (1-2kg capacity)

You're ready to order! 🚀