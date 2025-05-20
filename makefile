# Makefile for Cammander-in-Chief

# Variables
# Python interpreter
PYTHON := .venv/bin/python
# Remote Raspberry Pi project directory
PI_REPO_PATH := ~/Documents/repos/Cammander-in-Chief
PI_HOST := diego@raspberrypi.local

.PHONY: up-vpn down-vpn restart-vpn status-vpn start-server get-ip \
        connect-2-raspberrypi reboot-raspberrypi shutdown-raspberrypi \
        manual-update-raspberrypi uptime-raspberrypi

# === WireGuard VPN ===

up-vpn:
	sudo wg-quick up wg0
	@echo "VPN started."

down-vpn:
	sudo wg-quick down wg0
	@echo "VPN stopped."

restart-vpn: down-vpn up-vpn

status-vpn:
	sudo wg show
	@echo "VPN status displayed."

show-server-config:
	@sudo cat /etc/wireguard/wg0.conf

# === Flask App ===

flask-start:
	$(PYTHON) backend/app.py
	@echo "Flask server running at http://0.0.0.0:5000"

# === Utilities ===

get-ip:
	@curl -4 ifconfig.me
	@echo "\nPublic IPv4."

# === Raspberry Pi Server Control ===

connect-2-raspberrypi:
	@ssh -t $(PI_HOST) 'cd $(PI_REPO_PATH) && exec bash'

reboot-raspberrypi:
	@ssh $(PI_HOST) 'sudo reboot'

shutdown-raspberrypi:
	@ssh $(PI_HOST) 'sudo poweroff'

manual-update-raspberrypi:
	@ssh $(PI_HOST) 'sudo apt update && sudo apt upgrade -y'

uptime-raspberrypi:
	@ssh $(PI_HOST) 'uptime'

