# Makefile for Cammander-in-Chief

# variables
# Python interpreter
PYTHON := /usr/bin/python3

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

autostart-vpn:
	@sudo systemctl enable wg-quick@wg0
	@echo "Creating wg-monitor.service..."
	echo "[Unit]" | sudo tee /etc/systemd/system/wg-monitor.service > /dev/null
	echo "Description=WireGuard permanent Interface Monitor" | sudo tee -a /etc/systemd/system/wg-monitor.service > /dev/null
	echo "After=network.target" | sudo tee -a /etc/systemd/system/wg-monitor.service > /dev/null
	echo "" | sudo tee -a /etc/systemd/system/wg-monitor.service > /dev/null
	echo "[Service]" | sudo tee -a /etc/systemd/system/wg-monitor.service > /dev/null
	echo "ExecStart=$(HOME)/Documents/repos/Cammander-in-Chief/utils/wg-monitor.sh" | sudo tee -a /etc/systemd/system/wg-monitor.service > /dev/null
	echo "Restart=always" | sudo tee -a /etc/systemd/system/wg-monitor.service > /dev/null
	echo "RestartSec=10" | sudo tee -a /etc/systemd/system/wg-monitor.service > /dev/null
	echo "" | sudo tee -a /etc/systemd/system/wg-monitor.service > /dev/null
	echo "[Install]" | sudo tee -a /etc/systemd/system/wg-monitor.service > /dev/null
	echo "WantedBy=multi-user.target" | sudo tee -a /etc/systemd/system/wg-monitor.service > /dev/null

	@echo "Setting permissions and reloading systemd..."
	sudo chmod +x $(HOME)/Documents/repos/Cammander-in-Chief/utils/wg-monitor.sh
	sudo systemctl daemon-reload
	sudo systemctl enable wg-monitor.service
	sudo systemctl start wg-monitor.service

camera-streams:
	$(PYTHON) utils/define_camera_streams.py

.PHONY: up-vpn down-vpn restart-vpn status-vpn start-server get-ip autostart-vpn camera-streams
