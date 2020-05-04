import time
import zmq
from Crypto.Cipher import DES


def ECB(message,block_size,key):
    #each character is a byte in our case!
    key = bytes(key,'utf-8')
    message = bytes(message,'utf-8')
    cipher = DES.new(key, DES.MODE_ECB)
    msg = cipher.encrypt(message)
    return msg

def CBC(message,block_size,key):
    key = bytes(key,'utf-8')
    message = bytes(message,'utf-8')
    cipher = DES.new(key, DES.MODE_CBC)
    msg = cipher.encrypt(message)
    return msg


def CFB(message,block_size,key):
    key = bytes(key,'utf-8')
    message = bytes(message,'utf-8')
    cipher = DES.new(key, DES.MODE_CFB)
    msg = cipher.encrypt(message)
    return msg

def CTR(message,block_size,key):
    key = bytes(key,'utf-8')
    message = bytes(message,'utf-8')
    cipher = DES.new(key, DES.MODE_CTR)
    msg = cipher.encrypt(message)
    return msg
def create_tmp_messages(message):
    l = []
    for i in range(1,11):
        l.append(message*i)
    return l


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


print("Choose the mode of operation: ECB, CBC, CFB, CTR")
mode = input()
print(mode)

key = "the key!"
message = "hello there you "
block_size = 8
messages = create_tmp_messages(message)
i = 0

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request ",message)
    #  Do some 'work'
    time.sleep(1)
    if(i == 0):
        socket.send(bytes(mode,'utf-8'))
        i += 1
    else:
        if(mode == "ECB"):
            encrypted_message = ECB(messages[i-1],block_size,key)
        elif(mode == "CBC"):
            encrypted_message = ECB(messages[i-1],block_size,key)
        elif(mode == "CFB"):
            encrypted_message = ECB(messages[i-1],block_size,key)
        elif(mode == "CTR"):
            encrypted_message = ECB(messages[i-1],block_size,key)
        socket.send(encrypted_message)
        i += 1