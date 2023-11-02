working_dir = '/home/dark/Desktop/gian'
import textwrap
import time
import socket
import os
import json


from zipfile import ZipFile 
# working_dir = os.getcwd()
def extract(zip_directory, extract_location):
    with ZipFile(zip_directory, 'r') as zObject: 
          zObject.extractall(path=extract_location) 
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
        self.config_dir = f"/etc/apache2/sites-available"
        
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
        config = f"""Listen {self.port}\n<VirtualHost *:{self.port}>\n\tServerAdmin webmaster@localhost\n\tDocumentRoot {server_path}\n\t<Directory {server_path}>\n\t\tOptions Indexes FollowSymLinks\n\t\tAllowOverride All\n\t\tRequire all granted\n\t</Directory>\n\tErrorLog {panel_dir}/error.log\n\tCustomLog {panel_dir}/access.log combined\n</VirtualHost>"""
        with open(f"{config_dir}/{self.product_name}_{self.product_code}.conf", "w") as server_config_writer:
            server_config_writer.write(config)
            server_config_writer.close()

        print(config)

        #step_05 enabling the config file

        command = f"cd {config_dir} && sudo a2ensite {self.product_name}_{self.product_code}.conf"

        os.system(command)
        del command
        os.system("sudo systemctl reload apache2")
        os.system(f"mv {working_dir}/cgi-bin/serverdb/requestdata/{self.product_code}.json {working_dir}/cgi-bin/serverdb/requestdata/hosted/{self.product_code}_hosted.json")
        
        def purge(self):
            os.system(f"cd {config_dir} && sudo a2dissite {self.product_name}_{self.product_name}.conf")
            os.system(f"sudo rm {config_dir}/{self.product_name}_{self.product_code}.conf")
            os.system(f"sudo systemctl reload apache2")
            

while True:

    requested_data = os.listdir(f"{working_dir}/cgi-bin/serverdb/requestdata")
    if len(requested_data) > 1:
        for i in requested_data:
            if ".json" in i:
                print(i)
                product_code = i.split("+")[0].split(".")[0]
                print(product_code)
                deploying = ServerHost(product_code)
                deploying.config_loader()
                deploying.server_files_extract()
                deploying.apache_deploy()
                time.sleep(60)
            else:
                print("No server request found in requestdata")

    else:
        print("No server request found in requestdata")
        time.sleep(30)

        # hosted_data = os.listdir(f"{working_dir}/cgi-bin/serverdb/requestdata/hosted")
        # if len(hosted_data) > 0:
        #     for i in hosted_data:
        #         if ".json" in i:
