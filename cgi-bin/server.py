#!/usr/bin/python3
import sys
import cgi
import func
import os
import random
import json
import cgitb; cgitb.enable()
working_directory = os.getcwd()
formData = cgi.FieldStorage()
print("")
# Get filename here.
fileitem = formData['file']
# Test if the file was uploaded

if fileitem.filename:
   # strip leading path from file name to avoid
   # directory traversal attacks
    fn = os.path.basename(fileitem.filename)
    open(f'{working_directory}/' + fn, 'wb').write(fileitem.file.read())
    message = 'The file "' + fn + '" was uploaded successfully'

else:
   message = 'No file was uploaded'
print(message)

sys.exit()
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
        open(f'{working_directory}/serverdb/storage' + 'product_code.zip', 'wb').write(fileitem.file.read())
        message = 'The file "' + fn + '" was uploaded successfully'
    else:
        message = 'No file was uploaded'
        print(message)
    data = {
        "application": server_selection,
        "port": port,
        "project_name": nickname,
        "product_code": product_code,
        "server_files": fn
        }
    json_object = json.dumps(data, indent=4)
    with open(f"{working_directory}/serverdb/requestdata/{product_code}.json") as request_logger:
        request_logger.write(json_object)
        request_logger.close()
    print("Created a server")

    pass
else:
    print("")
    print("Invalid Session")

