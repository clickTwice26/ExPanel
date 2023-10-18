#!/usr/bin/python3
import sys
import cgi
import func
import os
import random
import json
import cgitb;
working_directory = os.getcwd()
formData = cgi.FieldStorage()
print("")
# Get filename here.
fileitem = formData['file']
# Test if the file was uploaded



# Test if the file was uploaded

server_selection = formData.getvalue("server_selection")
port = formData.getvalue("port")
nickname = formData.getvalue("nickname")
token = formData.getvalue("token")
if token.split("+")[1] == "server_create":
    pass
else:
    print("")
    print("Wrong token entered")
if func.security_check(token.split("+")[0], token.split("+")[1]):
    print("")
    product_code = random.randint(111111111,999999999)
    func.log(f"{port} {server_selection} {nickname}")
    if fileitem.filename:
        fn = os.path.basename(fileitem.filename)
        str(fn).replace("+","_")
        open(f'{working_directory}/cgi-bin/serverdb/storage/{product_code}+{fn}', 'wb').write(fileitem.file.read())
        message = 'The file "' + fn + '" was uploaded successfully'
        
    else:
        message = 'No file was uploaded'.str
    print(message)
    data = {
        "application": server_selection,
        "port": port,
        "project_name": nickname,
        "product_code": product_code,
        "server_files": fn
        }
    
    json_object = json.dumps(data, indent=4)
    with open(f"{working_directory}/cgi-bin/serverdb/requestdata/{product_code}.json", "w") as request_logger:
        request_logger.write(json_object)
        request_logger.close()
    # deployer = func.ServerHost(product_code)
    # deployer.config_loader()
    # deployer.server_files_extract()
    # deployer.apache_deploy()
    print("Created a server")
else:
    print("")
    print("Invalid Session")

