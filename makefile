# Makefile for Cammander-in-Chief

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

start-flask:
	cd backend && FLASK_APP=app.py flask run --host=0.0.0.0 --port=5000
	@echo "Flask server running at http://0.0.0.0:5000"

# === Utilities ===

get-ip:
	@curl -4 ifconfig.me
	@echo "\nPublic IPv4."

.PHONY: up-vpn down-vpn restart-vpn status-vpn start-server get-ip
