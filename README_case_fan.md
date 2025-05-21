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
