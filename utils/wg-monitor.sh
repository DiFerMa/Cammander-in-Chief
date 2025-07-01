#!/bin/bash

while true; do
    if ! ip link show wg0 > /dev/null 2>&1; then
        logger "[wg-monitor] WireGuard interface wg0 is down. Restarting..."
        /usr/bin/systemctl restart wg-quick@wg0
    fi
    sleep 90
done
