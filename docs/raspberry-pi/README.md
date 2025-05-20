# Raspberry Pi 4 Lite quick & short guide.

## Short intro

This is a quick guide I put together while setting up my own Raspberry Pi 4 with Raspberry Pi OS Lite. I wanted to cover the basics: SSH hardening, firewall (TBD since i want to evaluate it with wireguard yet), automatic updates, and some handy Makefile targets to manage it all remotely.

It's meant to be just enough to get things working safely and efficiently. If you're following along, I definitely recommend looking into each area more if you want to go deeper or adapt it to your setup.

## System considerations

- OS: Raspberry Pi with OS Lite (Debian 12 `bookworm`)
    - Headless install (meaning no UI environment, only console)
- Custom username and password (not default `pi`)
- Connected via SSH from Linux PC on same LAN

### Keep system updated automatically:
<code_block start>
sudo apt update && sudo apt upgrade
<code_block end>



## 🔐 SSH Hardening

### Edited SSH config at `/etc/ssh/sshd_config`:
<code_block start>
PasswordAuthentication no
PermitRootLogin no
ChallengeResponseAuthentication no
UsePAM yes
<code_block end>

### Effect:
- Password login **disabled**
- Only **SSH key authentication** allowed
- Root login via SSH **disabled**

### Verified SSH key works:
<code_block start>
ssh user@raspberrypi.local
<code_block end>

### Tested:
- Reconnected from Linux PC without password prompt
- Confirmed SSH key used via `ssh -v`



## Firewall Configuration (WIP and not yet tested)

### Installed and configured UFW:
<code_block start>
sudo apt install ufw
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw enable
<code_block end>

### Verified:
<code_block start>
sudo ufw status
<code_block end>



## 🛡️ SSH Brute-Force Protection (Fail2Ban)

### Installed:
<code_block start>
sudo apt install fail2ban
<code_block end>

### Used default config (protects SSH out-of-the-box)

### Verified:
<code_block start>
sudo fail2ban-client status
sudo fail2ban-client status sshd
<code_block end>



## 🔄 Automatic Security Updates

### Installed and enabled unattended upgrades:
<code_block start>
sudo apt install unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades
<code_block end>

### Confirmed settings in `/etc/apt/apt.conf.d/20auto-upgrades`:
<code_block start>
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
<code_block end>

### Verified correct source in `/etc/apt/apt.conf.d/50unattended-upgrades`:
<code_block start>
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
};
<code_block end>

### Verified correct distro and mirror:
<code_block start>
lsb_release -a
apt-cache policy
<code_block end>



## 📁 Basic File Structure Setup

### Created directories:
<code_block start>
mkdir ~/Documents ~/Downloads ~/Projects ~/Scripts
<code_block end>



## 🧼 System & Session Commands

### Exit SSH session:
<code_block start>
exit
<code_block end>

### Reboot Raspberry Pi:
<code_block start>
sudo reboot
<code_block end>

### Power off Raspberry Pi:
<code_block start>
sudo poweroff
<code_block end>

### Reconnect from Linux PC:
<code_block start>
ssh user@raspberrypi.local
<code_block end>



## 🛠️ Makefile Targets for Remote Control

### Variables used in Makefile:
<code_block start>
PI_REPO_PATH := ~/Documents/repos/Cammander-in-Chief
PI_HOST := user@raspberrypi.local
<code_block end>

### Connect to the Raspberry Pi and open a shell in the repo:
<code_block start>
make connect-2-raspberrypi
<code_block end>

This uses SSH to connect and `cd` into the specified project directory on the Pi, starting an interactive shell there.

### Reboot the Raspberry Pi remotely:
<code_block start>
make reboot-raspberrypi
<code_block end>

Sends a `sudo reboot` command via SSH.

### Shutdown the Raspberry Pi remotely:
<code_block start>
make shutdown-raspberrypi
<code_block end>

Gracefully powers off the Pi using `sudo poweroff` over SSH.

### Update the Raspberry Pi system:
<code_block start>
make manual-update-raspberrypi
<code_block end>

Runs:
<code_block start>
sudo apt update && sudo apt upgrade -y
<code_block end>
via SSH, to apply all package updates remotely.

### Check Pi uptime remotely:
<code_block start>
make uptime-raspberrypi
<code_block end>

Shows system uptime via SSH using the `uptime` command.



## ✅ Final State Summary

| Component         | Status              | Notes                                      |
|||--|
| Custom user       | ✔️                  | Non-default username                       |
| SSH hardened      | ✔️                  | Key-only login, root disabled              |
| Firewall (UFW)    | ✔️                  | SSH allowed, rest blocked                  |
| Fail2Ban          | ✔️                  | Defaults active, protects SSH              |
| Auto-updates      | ✔️                  | Security-only, official sources verified   |
| Session control   | ✔️                  | Commands to reboot, shut down, reconnect   |
| File structure    | ✔️                  | User directories created                   |
| Remote control    | ✔️                  | Make targets for SSH-based Pi management   |
