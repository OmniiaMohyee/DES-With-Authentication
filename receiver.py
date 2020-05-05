import zmq
from Crypto.Cipher import DES
from Crypto.Hash import CMAC

context = zmq.Context()

#  Socket to talk to server
print("Connecting to sender~")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

def convert_number(num):
    l = []
    for i in range(8):
        l.append(0)

    l[7] = num
    result = bytes(l)
    return result

def split_message(message):
    l = []
    for i in range(int(len(message)/8)):
        l.append(message[i*8:i*8+8])
    return l

def xor(ba1, ba2):
    return bytes(_a ^ _b for _a, _b in zip(ba1, ba2))

def CBC(message,key):
    key = bytes(key,'utf-8')
    cipher = DES.new(key, DES.MODE_ECB)
    list_mess = split_message(message)
    iv = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    mess = []
    for i in range(len(list_mess)):
        tmp = cipher.decrypt(list_mess[i])
        tmp = xor(tmp,iv)
        mess.append(tmp)
        iv = list_mess[i]
    result = ""
    for i in range(len(mess)):
        result += mess[i].decode('utf-8')
    return result

def ECB(message,key):
    key = bytes(key,'utf-8')
    cipher = DES.new(key, DES.MODE_ECB)
    list_mess = split_message(message)
    mess = []
    for i in range(len(list_mess)):
        mess.append(cipher.decrypt(list_mess[i]))
    result = ""
    for i in range(len(mess)):
        result += mess[i].decode('utf-8')
    return result

def CFB(message,key):
    key = bytes(key,'utf-8')
    cipher = DES.new(key, DES.MODE_ECB)
    list_mess = split_message(message)
    iv = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    mess = []
    for i in range(len(list_mess)):
        tmp = cipher.encrypt(iv)
        tmp = xor(list_mess[i],tmp)
        mess.append(tmp)
        iv = list_mess[i]
    result = ""
    for i in range(len(mess)):
        result += mess[i].decode('utf-8')
    return result

def CTR(message,key):
    key = bytes(key,'utf-8')
    list_mess = split_message(message)
    cipher = DES.new(key, DES.MODE_ECB)
    mess = []
    for i in range(len(list_mess)):
        tmp = cipher.encrypt(convert_number(i))
        tmp = xor(tmp,list_mess[i])
        mess.append(tmp)
    result = ""
    for i in range(len(mess)):
        result += mess[i].decode('utf-8')
    return result

key = "the key!"
mode = 0
secret = b'eightkey'
cobj = CMAC.new(secret, ciphermod=DES)
mac = ""
other_mac = ""
#  Do 10 requests, waiting each time for a response
for request in range(3):
    print("Sending request : ", request)
    socket.send(b"send next~")
    if(request == 0):
        mode = socket.recv()
        print(mode)
        mode = mode.decode('utf-8')
    elif(request == 1):
        mac = socket.recv()
    else:
        encrypted_message = socket.recv()
        cobj.update(encrypted_message)
        other_mac = bytes(cobj.hexdigest(),'utf-8')
        if(other_mac == mac):
            print("The message is authentic")
        else:
            print("The message or the key is wrong")
        if(mode == "ECB"):
            message = ECB(encrypted_message,key)
        elif(mode == "CBC"):
            message = CBC(encrypted_message,key)
        elif(mode == "CFB"):
            message = CFB(encrypted_message,key)
        elif(mode == "CTR"):
            message = CTR(encrypted_message,key)
        print(message)
        
    