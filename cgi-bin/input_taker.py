#!/usr/bin/python3
import cgi
data = cgi.FieldStorage()
duration = data.getvalue("duration")
username = data.getvalue("username")
with open("storage", "a") as data_writer:
    data_writer.write(str(duration)+str(username)+"\n")
    data_writer.close()
