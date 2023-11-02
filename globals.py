import sys
import socket
import os
import requests
import shutil
import json
from datetime import datetime
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
def portcheck(port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    location = ("127.0.0.1", port)
    result_of_check = a_socket.connect_ex(location)

    if result_of_check == 0:
        a_socket.close()
        return True
    
    else:
        a_socket.close()
        return False    
def clientSetup(session):
    console_log(f"Working Directory:{os.getcwd()}", session)
    console_log("Server Port: 8989", session)
    if portcheck("8989"):
        console_log("8989 Port is busy", session)
        sys.exit("Exiting Inappropriately")
    else:
        pass
    client_data = {
    "working_dir": os.getcwd(),
    "version": "alpha",
    "debug_out": "True",
    "console_logs": "True",
    "port": "8989"
}
    try:
        console_log("Client_Info Writer Successfull")

        with open("client.json", "w") as client_config_writer:
            client_config_writer.write(json.dumps(client_data,indent=4))
            client_config_writer.close()
    except Exception:
        console_log("Client_Info Writer failed")
    
def console_log(comment, session):
    working_dir = os.getcwd()
    debug_out_prompt = json.load(open("config.json", "r"))["debug_out"]
    if "warning" in comment or "error" in comment:
        debug_sign = "X"
    elif "unknown" in comment:
        debug_sign = "?"
    else:   
        debug_sign = "!"
    comment = f"[{debug_sign}] [{currenttime('both')}] [{comment}]"
    if debug_out_prompt == "True":
        debug_out = f"[DEBUG-{session}] {comment}"
        print(debug_out)
    else:
        pass
    debug_out_save = json.load(open("config.json", "r"))["console_logs"]
    if debug_out_save == "True":
        if os.path.exists(f"{working_dir}/debug_logs/console_{session}.log"):
            with open(f"{working_dir}/debug_logs/console_{session}.log", "a") as debug_logger:
                debug_logger.write(comment+"\n")
                debug_logger.close()
        else:
            with open(f"{working_dir}/debug_logs/console_{session}.log", "w") as debug_logger:
                debug_logger.write(comment+"\n")
                debug_logger.close()
    else:
        pass
    
def debug_clear():
    debug_dir = f"{os.getcwd()}/debug_logs/"
    os.system(f"rm -r {debug_dir}*")
def deployer_set(session):
    client_data = json.load(open("config.json", "r"))
    working_dir = os.getcwd()
    
    unset_deployer_data =  open("base_deployer", "r").read()
    new_Data = f"working_dir = '{client_data['working_dir']}'\n"
    new_Data = new_Data+unset_deployer_data
    # print(new_Data)
    try:
        with open("deployer.py", "w") as deployer:
            deployer.write(new_Data)
            deployer.close()
            console_log("deployer file successfully created", session)
    except Exception as error:
        console_log("error faced during creating deployer file: {}".format(error), session)
    try:
        shutil.copy(f"{working_dir}/deployer.py", "/bin/")
        console_log("Deployer installation successfull", session)
    except Exception as error:
        console_log("Deployer installation to the bin folder unsuccessfull. error is:{}".format(error), session)
    deployer_service_file = f"""[Unit]
Description=XpanelDeployer

[Service]
User=root
WorkingDirectory=/bin
ExecStart=/usr/bin/python3 /bin/deployer.py
# optional items below
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
    
    
    """
    server_service_file = f"""[Unit]
Description=XpanelDeployer

[Service]
User=root
WorkingDirectory={working_dir}
ExecStart=/usr/bin/python3 {working_dir}/server.py
# optional items below
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target"""
    # print(service_file)
    with open("xpanel_deployer.service", "w") as service_writer:
        service_writer.write(deployer_service_file)
        service_writer.close()
    with open("xpanel_server.service", "w") as server_service_writer:
        server_service_writer.write(server_service_file)
        server_service_writer.close()
        
    try:
        shutil.copy("xpanel_deployer.service", "/etc/systemd/system/")
        shutil.copy("xpanel_server.service", "/etc/systemd/system/")
    except Exception as error:
        print(error)

def requirements():
    pass    