## ✅ Common NPN BJTs (Good for GPIO control of small loads)
Look for these part numbers:
- 2N2222 / PN2222
- BC547 / BC548 / BC549
- S8050
- TIP120 / TIP122 (Darlington, overkill but works)
- 2SC1815
- C945 (popular in older gear)
- BD139 (larger power handling)

🔌 Note: BJTs need a base resistor (1kΩ is a good starting value).

## ✅ Common Logic-Level N-Channel MOSFETs (More efficient switching)
These are ideal for GPIO control, as they turn fully on with 3.3V:
- IRLZ44N
- IRL540N
- IRL3705
- IRL520
- AO3400 / AO3407
- IRF3708 (logic-level)

🧠 Important: IRF parts like IRF540 or IRFZ44N are not logic-level — they need ~10V to switch properly and don’t work well with 3.3V GPIO. Only the IRL (logic-level) versions do.

## ❌ Components to Skip (Not suitable or unsafe)
- PNP transistors (e.g., BC557) — harder to use for ground-side switching
- PMOS devices (not ideal for GPIO control without level shifting)
- SCRs / Triacs — for AC switching only
- Any component marked as “high voltage only”

## 🧪 How to Identify:
Look at the part number printed on each transistor and Google it along with “datasheet” — check for:
- Type: NPN or N-MOSFET
- V_GS(th) (MOSFETs): Must be ≤ 2V to fully turn on with 3.3V GPIO
- Max collector/emitter current: Should be ≥ 200 mA

If you're unsure about a part, send me its marking and I’ll check it for you.

## Optional: Add a Diode
Put a diode (like 1N4007) across the fan terminals (stripe toward +) for flyback protection — especially helpful for inductive loads like fans or motors.







# 🧰 Raspberry Pi Fan Control – Notes for Setup

## ✅ Software Requirements

Install necessary packages:

<code_start>
sudo apt update
sudo apt install python3 python3-gpiozero
<code_end>

Make sure your user has GPIO access (usually default for `pi` user).

---

## 🐍 Python Script: fan_controller.py

Create the following file:

<code_start>
nano /home/pi/fan_controller.py
<code_end>

Paste this content:

<code_start>
from gpiozero import OutputDevice
import time

FAN_PIN = 18  # GPIO pin controlling the fan
ON_TEMP = 60  # Temperature (°C) to turn fan ON
OFF_TEMP = 50  # Temperature (°C) to turn fan OFF

fan = OutputDevice(FAN_PIN)

def get_temp():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        return int(f.read()) / 1000.0

while True:
    temp = get_temp()
    if temp > ON_TEMP:
        fan.on()
    elif temp < OFF_TEMP:
        fan.off()
    time.sleep(5)
<code_end>

Make it executable (optional):

<code_start>
chmod +x /home/pi/fan_controller.py
<code_end>

---

## ⚙️ Auto-Start at Boot with systemd

Create a new systemd service:

<code_start>
sudo nano /etc/systemd/system/fancontrol.service
<code_end>

Paste the following:

<code_start>
[Unit]
Description=Raspberry Pi Fan Controller
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/fan_controller.py
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
<code_end>

Enable and start the service:

<code_start>
sudo systemctl daemon-reexec
sudo systemctl enable fancontrol.service
sudo systemctl start fancontrol.service
<code_end>

Check status:

<code_start>
systemctl status fancontrol.service
<code_end>

To stop or disable:

<code_start>
sudo systemctl stop fancontrol.service
sudo systemctl disable fancontrol.service
<code_end>

---

## ✅ Summary

- Python script reads CPU temp and toggles GPIO pin for the fan.
- Runs automatically on boot via systemd.
- Lightweight and safe.


## ✅ Wiring Instructions for Fan Control Using NPN Transistor (e.g., 2N2222 or BC547)

### 🔌 POWER & FAN

1. **+5V pin on Raspberry Pi GPIO header**  
   → connect to **red wire (positive +) of the fan**

2. **Black wire (negative –) of the fan**  
   → connect to the **collector pin of the NPN transistor**

---

### ⚙️ TRANSISTOR CONNECTIONS

3. **Emitter pin of the NPN transistor**  
   → connect to **GND pin on the Raspberry Pi GPIO header**

4. **Base pin of the NPN transistor**  
   → connect to a **1kΩ resistor**

5. The **other end of the 1kΩ resistor**  
   → connect to a **free GPIO pin on the Raspberry Pi** (e.g., GPIO18)

---

### ⚡ FLYBACK DIODE (PROTECTION)

6. **Cathode (striped side) of the diode (e.g., 1N4007)**  
   → connect to the **red wire of the fan** (same point as the 5V connection)

7. **Anode (non-striped side) of the diode**  
   → connect to the **black wire of the fan** (same point as collector of the transistor)

---

## 🧠 Summary of Connections

| Component                | Connects To                            |
|--------------------------|----------------------------------------|
| Fan red wire (+)         | Pi 5V pin                              |
| Fan black wire (–)       | Transistor collector                   |
| Transistor emitter       | Pi GND pin                             |
| Transistor base          | GPIO pin through 1kΩ resistor          |
| Diode cathode (striped)  | Fan red wire / Pi 5V                   |
| Diode anode (non-stripe) | Fan black wire / transistor collector  |

