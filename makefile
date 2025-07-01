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

review-vpn-downtimes:
	@echo
	@journalctl -u wg-monitor.service --since "1 hours ago"
	@echo
	@echo "NOTE: Adjust the desired time range accordingly"
	@echo
	@echo "WARNING: If your see in the above lines logs like these:"
	@echo "	<time_stamp> raspberrypi systemd[1]: wg-monitor.service: Scheduled restart job, restart counter is at 5827."
	@echo "	<time_stamp> raspberrypi systemd[1]: Stopped wg-monitor.service - WireGuard permanent Interface Monitor."
	@echo "	<time_stamp> raspberrypi (nitor.sh)[20458]: wg-monitor.service: Failed to locate executable <path/to>/wg-monitor.sh:>"
	@echo "	<time_stamp> raspberrypi (nitor.sh)[20458]: wg-monitor.service: Failed at step EXEC spawning <path/to>/wg-monitor.sh>"
	@echo "	<time_stamp> raspberrypi systemd[1]: Started wg-monitor.service - WireGuard permanent Interface Monitor."
	@echo "	<time_stamp> raspberrypi systemd[1]: wg-monitor.service: Main process exited, code=exited, status=203/EXEC"
	@echo "	<time_stamp> raspberrypi systemd[1]: wg-monitor.service: Failed with result 'exit-code'."
	@echo "Then, you could be wearing out your sd if many logs are written."
	@echo "Check that 'wg-monitor.sh' is executable."

auto-start-flask:
	@echo "Creating cammanager.service..."
	echo "[Unit]" | sudo tee /etc/systemd/system/cammanager.service > /dev/null
	echo "Description=Camera System Manager (main.py)" | sudo tee -a /etc/systemd/system/cammanager.service > /dev/null
	echo "After=network.target" | sudo tee -a /etc/systemd/system/cammanager.service > /dev/null
	echo "" | sudo tee -a /etc/systemd/system/cammanager.service > /dev/null
	echo "[Service]" | sudo tee -a /etc/systemd/system/cammanager.service > /dev/null
	echo "ExecStart=/usr/bin/python3 $(HOME)/Documents/repos/Cammander-in-Chief/main.py" | sudo tee -a /etc/systemd/system/cammanager.service > /dev/null
	echo "WorkingDirectory=$(HOME)" | sudo tee -a /etc/systemd/system/cammanager.service > /dev/null
	echo "Restart=always" | sudo tee -a /etc/systemd/system/cammanager.service > /dev/null
	echo "User=diego" | sudo tee -a /etc/systemd/system/cammanager.service > /dev/null
	echo "Environment=PYTHONUNBUFFERED=1" | sudo tee -a /etc/systemd/system/cammanager.service > /dev/null
	echo "" | sudo tee -a /etc/systemd/system/cammanager.service > /dev/null
	echo "[Install]" | sudo tee -a /etc/systemd/system/cammanager.service > /dev/null
	echo "WantedBy=multi-user.target" | sudo tee -a /etc/systemd/system/cammanager.service > /dev/null

	@echo "Reloading systemd and enabling cammanager.service..."
	sudo systemctl daemon-reload
	sudo systemctl enable cammanager.service
	sudo systemctl start cammanager.service

review-flask-autostart:
	@echo
	@journalctl -u cammanager.service

define-camera-streams:
	$(PYTHON) utils/define_camera_streams.py

.PHONY: up-vpn down-vpn restart-vpn status-vpn start-server get-ip autostart-vpn camera-streams
