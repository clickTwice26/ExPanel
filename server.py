import os
import json

client_data = json.load(open("client.json"), "r")
port = client_data["port"]
os.system(f"python3 -m http.server --cgi {port}")