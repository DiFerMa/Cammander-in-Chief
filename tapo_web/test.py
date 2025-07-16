from pytapo import Tapo

tapo = Tapo("192.168.178.51", "tapoc51a", "=Gabyhalo45")
#tapo = Tapo("192.168.178.52", "tapoc500", "=Gabyhalo45")

try:
    print("Trying to get device info...")
    print(tapo.getBasicInfo())  # or getBasicInfo()
except Exception as e:
    print("❌ API error:", e)

try:
    for mode in ("on", "off", "auto"):
        print(f"\nSetting vision mode to '{mode}'...")
        tapo.setDayNightMode(mode)
        current = tapo.getDayNightMode()
        print("Mode is now:", current)
except Exception as e:
    print("❌ API error:", e)
