# IP-Storyline (Trace — IP Address Lookup)

A Flask-based IP and domain lookup web application that takes an IP address or domain name, resolves it to an IP address, classifies public vs. private IP ranges, performs reverse DNS (`PTR`) lookups, retrieves ISP and geolocation metadata from `ip-api.com`, and checks basic HTTP reachability.

## Overview

When troubleshooting networks or inspecting unknown hosts, it helps to see several basic signals in one place: whether an input resolves, whether the resulting IP is private or public, what reverse DNS hostname maps back to it, which ISP or organization owns the address, and whether a basic HTTP request gets a response. **IP-Storyline** wraps these checks into a lightweight Flask web interface (`Trace — IP Address Lookup`) backed by Python's standard networking libraries and `requests`.

## Features

- **Flexible Input Resolution:** Accepts either an IP address (`ipaddress.ip_address`) or a domain name (`socket.gethostbyname`), resolving domains to their IPv4 address when possible.
- **Public vs. Private IP Classification:** Uses Python's `ipaddress` module (`is_private`) to distinguish private/internal addresses from public addresses.
- **Reverse DNS (`PTR`) Lookup:** Queries `socket.gethostbyaddr(ip)` to return the reverse hostname when a PTR record exists, or reports that none was found.
- **Geolocation & Network Metadata:** Fetches details from `http://ip-api.com/json/{ip}`, including ISP, city, country, hostname, ZIP code, timezone, and organization.
- **Reachability Check:** Sends an HTTP `GET` request with a timeout to report whether the target responds with HTTP `200`, returns another status code, or appears down/unreachable.
- **Web Interface:** Renders a form and result view through Flask's `render_template("index.html", result=result)`.

## How It Works

1. **Input Submission (`POST /`):** The user enters an IP address or domain into the form field `ip`.
2. **Resolution (`resolve_input`):**
   - First attempts to parse the input as a valid IP address using `ipaddress.ip_address`.
   - If that raises `ValueError`, treats the input as a domain name and calls `socket.gethostbyname` (catching `socket.gaierror` if resolution fails).
3. **IP Classification (`check_ip_type`):** Checks whether the resolved IP is private (`Private IP`) or public (`Public IP`).
4. **Reverse DNS (`reverse_dns_lookup`):** Calls `socket.gethostbyaddr(ip)` and gracefully handles `socket.herror` when no reverse DNS record is available.
5. **Metadata Lookup (`get_ip_details`):** Queries `ip-api.com`'s JSON endpoint and extracts `ISP`, `City`, `Country`, `Hostname`, `Zip Code`, `Timezone`, and `Organization`.
6. **HTTP Status Probe (`check_domain_status`):** Performs a `requests.get(..., timeout=5)` check and formats a human-readable status message.
7. **Template Rendering:** Passes the compiled `result` dictionary (or an error dictionary if resolution fails) to `templates/index.html`.

## Project Structure

```text
IP-Storyline/
├── app.py              # Flask application, resolution/DNS/lookup helpers, and main route
├── requirements.txt    # Python dependencies (Flask, gunicorn, requests)
├── README.md           # Project documentation
├── .gitignore          # Ignored files and folders (.venv/, __pycache__/, .env, etc.)
├── templates/
│   └── index.html      # Main HTML template for input form and lookup results
└── static/             # Optional static assets (CSS, JS, images)
