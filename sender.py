import time
import zmq
from Crypto.Cipher import DES


def ECB(message,block_size,key):
    #each character is a byte in our case!
    key = bytes(key,'utf-8')
    print(len(message))
    message += ' '
    print(len(message))
    message = bytes(message,'utf-8')
    result = ""
    print(len(key))
    cipher = DES.new(key, DES.MODE_ECB)
    msg = cipher.encrypt(message)
    return msg

def CBC(message,block_size,key):
    return 1
def CFB(message,block_size,key):
    return 1
def CTR(message,block_size,key):
    return 1

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("Choose the mode of operation: ECB, CBC, CFB, CTR")
mode = input()
print(mode)

# alive = socket.recv()
# print("Received Alive Message: %s" % alive)

# time.sleep(1)
# socket.send(bytes(mode, 'utf-8'))

key = "the key!"
message = "hello, this is a dummy message to test with the different message of operation!"
encrypted_message = ""
block_size = 16
if(mode == "ECB"):
    encrypted_message = ECB(message,block_size,key)
elif(mode == "CBC"):
    encrypted_message = ECB(message,block_size,key)
elif(mode == "CFB"):
    encrypted_message = ECB(message,block_size,key)
elif(mode == "CTR"):
    encrypted_message = ECB(message,block_size,key)

print(encrypted_message)





    
