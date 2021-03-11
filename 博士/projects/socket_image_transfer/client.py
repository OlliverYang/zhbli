"""
Created on Fri Dec 13 13:12:56 2019
@author: hoang
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 11:54:37 2019
@author: hoang
"""

import socket
def wait_for_acknowledge(client,response):
    """
    Waiting for this response to be sent from the other party
    """
    amount_received = 0
    amount_expected = len(response)
    
    msg = str()
    while amount_received < amount_expected:
        data = client.recv(16)
        amount_received += len(data)
        msg += data.decode("utf-8")
        #print(msg)
    return msg

#initiate connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_addr = (socket.gethostname(), 2019)  #change here for sending to another machine in LAN
client.connect(server_addr)
print(f"Connected to server!")

client.settimeout(5) #limit each communication time to 5s

#listening to server command
print("Client is now waiting for server's command.")
cmd_from_server = wait_for_acknowledge(client,"Start sending image.")

#send an ACK 
imgCount_from_server = 0
if cmd_from_server == "Start sending image.":
    print("Command \"Start sending image.\" received.")
    print("Sending ACK...")
    client.sendall(bytes("ACK","utf-8"))
    try:
        print("Client is now waiting for the number of images.")
        imgCount_from_server = int(wait_for_acknowledge(client,str(3)))  
        
    except:
        raise ValueError("Number of images received is buggy.")

if imgCount_from_server > 0:
    print("Number of images to receive: ",imgCount_from_server)
    print("Sending ACK...")
    client.sendall(bytes("ACK","utf-8"))

print(f"Client is now eceiving {imgCount_from_server} images.")



for i in range(imgCount_from_server):
    index = i+1
    file = f"./imgfromserver{index}.jpg"
    try:                                            #check for existing file, will overwrite
        f = open(file, "x")           
        f.close()
    except:
        pass
    finally:
        f = open(file, "wb")
    print(f"\tReceiving image {index}")
    imgsize = int(wait_for_acknowledge(client,str(3)))
    print(f"\tImage size of {imgsize}B received by Client")
    print("Sending ACK...")
    client.sendall(bytes("ACK","utf-8"))  
    buff = client.recv(imgsize)
    f.write(buff)
    f.close()
    print(f"File {file} received!")
    print("Sending ACK...")
    client.sendall(bytes("ACK","utf-8"))
    #a = wait_for_acknowledge(client,"This is done.")

print("All images received.")
print("Closing connection.")
client.close()