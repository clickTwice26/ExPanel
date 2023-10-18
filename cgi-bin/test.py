import socket
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

print(portcheck(53))