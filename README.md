# IP-Storyline (Trace — IP Address Lookup)

A Flask-based web application that resolves IP addresses and domain names to provide IP classification (Public vs. Private), reverse DNS hostnames, geolocation/ISP metadata via `ip-api.com`, and basic HTTP reachability status.

## Features
- **IP & Domain Resolution:** Accepts either an IP address or a domain name and resolves it to an IP.
- **IP Type Detection:** Distinguishes between public and private IP addresses using Python's `ipaddress` module.
- **Reverse DNS Lookup:** Queries hostname records (`PTR` / `socket.gethostbyaddr`) for resolved IPs.
- **Network & Geolocation Details:** Fetches ISP, city, country, hostname, ZIP code, timezone, and organization info from `ip-api.com`.
- **Reachability Check:** Tests HTTP connectivity to report whether the target responds or is unreachable.

## Tech Stack
- **Backend:** Python, Flask, Gunicorn
- **Networking & HTTP:** `socket`, `ipaddress`, `requests`, `ip-api.com`
- **Frontend:** HTML (`templates/index.html`) and CSS


