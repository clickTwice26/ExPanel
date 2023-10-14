import json
import os
import requests
from datetime import datetime
import socket
import pathlib
import random
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
def tokengen(timeframe):
    token = str(random.randint(1111111,99999999))+f"+{timeframe}"
    with open(f"{working_dir}/cgi-bin/tokens/{token}", "w") as tokenwriter:
        tokenwriter.write(f"Token Generated at: {currenttime('both')}")
        tokenwriter.close()
    return token
def tokendel(token, timeframe):
    try:
        os.remove(f"{working_dir}/tokens/{token}+{timeframe}")
    except:
        log(f"Token Deletion Unsuccessful : {token+timeframe}")
def log(comment):
    comment = f"[+] {currenttime()} - {comment}"
    with open("server_log.txt", "a") as logger:
        logger.write(comment+"\n")
        logger.close()


class ServerHost:
    def __init__(self, identity) -> None:
        self.request_data = json.load(identity)

        pass

def security_check(token,timeframe):
    
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    server_logs_directory = f"{working_dir}/server_logs/logs"

    token_list = os.listdir(f"{working_dir}/cgi-bin/tokens")

    if (token+"+"+timeframe) in token_list:
        tokenstatus = "Token Matched"
        status = True
        tokendel(token, timeframe)
    else:
        status = False
        tokenstatus = "Token Mismatched"

    if os.path.isfile(server_logs_directory):
        pass
    else:
        with open(server_logs_directory, "w") as server_logs_init:
            server_logs_init.write("")
            server_logs_init.close()
        

    #security_logs
    comment = f"[SECURITY CHECK] >> {host_name} | {ip_address} | {token+timeframe} | {tokenstatus}\n"
    with open(f"{working_dir}/server_logs/logs", "a") as server_logs:
        server_logs.write(comment)
        server_logs.close()
    return status
