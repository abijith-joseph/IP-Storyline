from flask import Flask, request, render_template
import socket #Used for network connections
import ipaddress #Understand and work with IP addresses
import requests #Send HTTP requests to web services
app = Flask(__name__)
def resolve_input(user_input):
    try: #Checks if the input is a valid IP address
        ip_obj=ipaddress.ip_address(user_input)
        return str(ip_obj)
    except ValueError:
        try: #If the input is a domain name,then it converts to its IP address
            return socket.gethostbyname(user_input) #domain name → IP address
        except socket.gaierror: #If the input is neither a valid ip address nor a valid domain name
            return None

def check_ip_type(ip): #Check if the input IP is Private or Public
    ip_obj=ipaddress.ip_address(ip)
    if ip_obj.is_private:
        return"Private IP"
    else:
        return "Public IP"

def get_ip_details(ip):
    url = f"http://ip-api.com/json/{ip}"#ip-api is a online service that gives detailed information about any public IP address or domain
    response = requests.get(url).json() #The APIs return data in JSON format, which is then converted into a Python dictionary using the .json() method.
    return {
        "ISP": response.get("isp"),
        "City": response.get("city"),
        "Country":response.get("country"),
        "Hostname":response.get("hostname"),
        "Zip Code":response.get("zip"),
        "Timezone":response.get("timezone"),
        "Organization":response.get("org")
    }

def reverse_dns_lookup(ip):
    try:
        hostname,alias,_=socket.gethostbyaddr(ip)
        return hostname
    except socket.herror: #herror → Host Error
        return "No reverse DNS found"

def check_domain_status(domain):
    try:
        response = requests.get(f"http://{domain}",timeout=5)
        if response.status_code == 200:
            return "Domain is UP"
        else:
            return f"Domain responded with status {response.status_code}"
    except requests.exceptions.RequestException:
        return " Domain is DOWN or unreachable"

@app.route("/", methods=["GET","POST"])
def lookup():
    result = None
    if request.method == "POST":
        user_input = request.form["ip"]
        ip = resolve_input(user_input)
        if ip:
            hostname = reverse_dns_lookup(ip)
            details = get_ip_details(ip)
            status = check_domain_status(ip)
            result = {
                "Resolved IP": ip,
                "IP Type": check_ip_type(ip),
                "Reverse DNS Hostname": hostname,
                "ISP": details['ISP'],
                "City": details['City'],
                "Country": details['Country'],
                "Zip Code": details['Zip Code'],
                "Timezone": details['Timezone'],
                "Organization": details['Organization'],
                "Status": status
            }
        else:
             result={"error":"Invalid input or Domain not found."}
    return render_template("index.html", result=result)
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



