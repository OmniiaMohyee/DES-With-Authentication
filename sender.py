import time
import zmq
from Crypto.Cipher import DES
from Crypto import Random
from Crypto.Hash import CMAC

def split_message(message):
    l = []
    for i in range(int(len(message)/8)):
        l.append(bytes(message[i*8:i*8+8],'utf-8'))
    return l

def xor(ba1, ba2):
    return bytes(_a ^ _b for _a, _b in zip(ba1, ba2))

def convert_number(num):
    l = []
    for i in range(8):
        l.append(0)

    l[7] = num
    result = bytes(l)
    return result

#WORKING!
def ECB(message,key):
    key = bytes(key,'utf-8')
    cipher = DES.new(key, DES.MODE_ECB)
    list_mess = split_message(message)
    tmp = cipher.encrypt(list_mess[0])
    for i in range(1,len(list_mess)):
        tmp += cipher.encrypt(list_mess[i])
    return tmp

def CBC(message,key):
    key = bytes(key,'utf-8')
    cipher = DES.new(key, DES.MODE_ECB)
    list_mess = split_message(message)
    iv = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    cipher_list = []
    for i in range(len(list_mess)):
        tmp = xor(list_mess[i],iv)
        tmp = cipher.encrypt(tmp)
        cipher_list.append(tmp)
        iv = tmp
    result = cipher_list[0]
    for i in range(1,len(cipher_list)):
        result += cipher_list[i]
    return result

def CFB(message,key):
    key = bytes(key,'utf-8')
    cipher = DES.new(key, DES.MODE_ECB)
    list_mess = split_message(message)
    iv = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    cipher_list = []
    for i in range(len(list_mess)):
        tmp = cipher.encrypt(iv)
        tmp = xor(list_mess[i],tmp)
        cipher_list.append(tmp)
        iv = tmp
    result = cipher_list[0]
    for i in range(1,len(cipher_list)):
        result += cipher_list[i]
    return result

def CTR(message,key):
    key = bytes(key,'utf-8')
    list_mess = split_message(message)
    cipher = DES.new(key, DES.MODE_ECB)
    cipher_list = []
    for i in range(len(list_mess)):
        tmp = cipher.encrypt(convert_number(i))
        tmp = xor(tmp,list_mess[i])
        cipher_list.append(tmp)

    result = cipher_list[0]
    for i in range(1,len(cipher_list)):
        result += cipher_list[i]
    return result

def create_tmp_messages(message):
    l = []
    for i in range(1,11):
        l.append(message*i)
    return l


print("Sender up~")
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


print("Choose the mode of operation: ECB, CBC, CFB, CTR")
mode = input()

key = "the key!"
message = ""
print("Enter test case file name:")
file_name = input()
with open(file_name, 'r') as file:
    message = file.read().replace('\n', '\n')
print(message)
if(len(message) % 8 != 0):
    for i in range(8-len(message)%8):
        message += ' '

secret = b'eightkey'
cobj = CMAC.new(secret, ciphermod=DES)

i = 0
while True:
    #  Wait for next request from client
    msg = socket.recv()
    print("Received request ",msg)
    time.sleep(1)
    if(i == 0):
        socket.send(bytes(mode,'utf-8'))
        i += 1
    
    else:
        if(mode == "ECB"):
            encrypted_message = ECB(message,key)
        elif(mode == "CBC"):
            encrypted_message = CBC(message,key)
        elif(mode == "CFB"):
            encrypted_message = CFB(message,key)
        elif(mode == "CTR"):
            encrypted_message = CTR(message,key)
        else:
            print("Mode not supported")
            break
        if (i == 1):
            cobj.update(encrypted_message)
            print(cobj.hexdigest())
            socket.send(bytes(cobj.hexdigest(),'utf-8'))
        if (i == 2):
            socket.send(encrypted_message)
        i += 1
        if (i == 3):
            break

