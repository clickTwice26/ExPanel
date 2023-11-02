import json
import os
import requests
from datetime import datetime
import socket
import pathlib
import random
import socket
from zipfile import ZipFile 
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
        


working_dir = os.getcwd()
def extract(zip_directory, extract_location):
    with ZipFile(zip_directory, 'r') as zObject: 
          zObject.extractall(path=extract_location) 

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


#index file save

def value_validator(configuration):
    test_result = []
    test_result_code = []
    if 1024 < int(configuration["port"]) < 65535:
        test_result.append(f"[+] Port under range {int(configuration['port'])}")
        if portcheck(int(configuration["port"])) is False:
            test_result.append(f"[+]Port:{int(configuration['port'])} is free to use")
            test_result_code.append(1)
        else:
            test_result.append("[+]Port is not available")
    else:
        test_result.append("[+]Ports out of range")
    





class ServerHost:
    def __init__(self, product_code) -> None:
        self.product_code = product_code

        
    def config_loader(self):
        configuration = json.load(open(f"{working_dir}/cgi-bin/serverdb/requestdata/{self.product_code}.json", "r"))
        self.port = configuration["port"]
        self.application = configuration["application"].lower()
        self.product_code = configuration["product_code"]
        self.product_name = configuration["project_name"]
        self.server_files = configuration["server_files"]
        self.root = str(self.product_code)+"+"+str(self.product_name)
        
    def server_files_extract(self):
        #importing deply configuration
        deploy_directory = f"{working_dir}/cgi-bin/deployment/{self.application}/{self.product_code}+{self.product_name}/"
        if not os.path.exists(deploy_directory):
            os.mkdir(deploy_directory)
        # os.mkdir(deploy_directory)
        
        
        extract(f"{working_dir}/cgi-bin/serverdb/storage/{self.product_code}+{self.server_files}", deploy_directory)


    def apache_deploy(self):
        #step_01
        
        
        server_configuration = json.load(open(f"{working_dir}/cgi-bin/serverdb/requestdata/{self.product_code}.json","r"))
        apache2_configuration = json.load(open(f"{working_dir}/cgi-bin/serverdb/deploy_configuration/{self.application}.json", "r"))
        # config_dir = apache2_configuration["config_dir"]
        ####

        # if apache2_configuration["default_disabled"] == "True":
        #     pass
        # else:
        #     print("You have to disable default configuration")
        server_path = f"{working_dir}/cgi-bin/deployment/{self.application}/{self.root}"
        panel_dir = f"{working_dir}/cgi-bin/serverdb/panel/{self.product_code}"
        if os.path.exists(panel_dir) is False:
            os.mkdir(panel_dir)


        #step_02
        # # command = f"sudo chown -R $USER:$USER {self.root}"
        # # command2 = f"sudo chmod -R {self.root}"
        # os.system(command+" && "+ command2)
        # del command
        #step_3 creating a sample index file
        #step_04 config
        config_dir = f"/etc/apache2/sites-available"
        bracket_open = "{"
        bracket_close = "}"
        config = f"""
        Listen {self.port}
        <VirtualHost *:{self.port}>
            ServerAdmin webmaster@localhost
            DocumentRoot {self.root}
            <Directory {self.root}>
                Options Indexes Follow SymLinks
                AllowOverride All
                Require all granted
            </Directory>

            ErrorLog ${bracket_open}{panel_dir}{bracket_close}/error.log
            CustomLog ${bracket_open}{panel_dir}{bracket_close}/access.log combined


        </VirtualHost>
        """
        with open(f"{config_dir}/{self.product_name}_{self.product_code}.conf", "w") as server_config_writer:
            server_config_writer.write(config)
            server_config_writer.close()

        print(config)

        #step_05 enabling the config file

        command = f"cd {config_dir} && sudo a2ensite {self.product_name}_{self.product_code}.conf"

        os.system(command)
        del command
        os.system("sudo systemctl reload apache2")
            

        
        


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
