import json
import os
import requests
from datetime import datetime
import socket
import pathlib
working_dir = os.getcwd()

def currenttime(outputl="both"):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if outputl == "date":
        dt_string = now.strftime("%d/%m/%Y")
        return str(dt_string)
    elif outputl == "time":
        dt_string = now.strftime("%H:%M:%S")
        return str(dt_string)
    else:
        return str(dt_string)
    

def log(comment):
    comment = f"[+] {currenttime()} - {comment}"
    with open("server_log.txt", "a") as logger:
        logger.write(comment+"\n")
        logger.close()


class ServerHost:
    def __init__(self, identity) -> None:
        self.request_data = json.load(identity)

        pass

def security_check(ip, token, timeframe):
    
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    server_logs_directory = f"{working_dir}+/server_logs/logs"
    if os.path.isfile(server_logs_directory):
        pass
    else:
        with open(server_logs_directory, "w") as server_logs_init:
            server_logs_init.write("")
            server_logs_init.close()
        

    #security_logs
    comment = f"[SECURITY CHECK] >> {host_name} | {ip_address} | "
    with open(f"{working_dir}+/server_logs/logs", "a") as server_logs:
        server_logs.write()
        server_logs.close()

