# GMX Creator

# Requirements
- Linux VPS Debian 12 (Any Specs)
- CapSolver API Key For IMAP
- CaptchaFox API Key For Register

# Install
- apt update && apt upgrade -y && apt install python3-pip -y
- pip install capsolver --break-system-packages
- pip install curl-cffi --break-system-packages
- pip install loguru --break-system-packages
- pip install asyncio --break-system-packages
- pip install logger --break-system-packages
- pip install aiohttp --break-system-packages

# Run
- put CapSolver API key here https://github.com/RUSOCIAL-SU/GMX-Creator/blob/main/main.py#L17 on your VPS
- put CaptchaFox API key here https://github.com/RUSOCIAL-SU/GMX-Creator/blob/main/main.py#L97 on your VPS
- put proxies in proxies.txt (Format username:password@ip:port) (Rotating Or 5-10 mins)
- python3 main.py

# Proxy Requirements / Recommendations
- Only USE USA PROXIES
- https://smartproxy.com is best for this but requires ID Upload
