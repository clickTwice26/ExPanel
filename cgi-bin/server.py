#!/usr/bin/python3
import cgi
import func
formData = cgi.FieldStorage()

server_selection = formData.getvalue("server_selection")
port = formData.getvalue("port")
nickname = formData.getvalue("nickname")

print("")
func.log(f"{port} {server_selection} {nickname}")
print("Created a server")