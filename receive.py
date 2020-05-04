import zmq
from Crypto.Cipher import DES

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

key = "the key!"
orig = DES.new(bytes(key,'utf-8'), DES.MODE_ECB)
mode = 0
#  Do 10 requests, waiting each time for a response
for request in range(11):
    print("Sending request : ", request)
    socket.send(b"Hello")
    if(request == 0):
        mode = socket.recv()
        print(mode.decode('utf-8'))
        if(mode == "ECB"):
            orig = DES.new(bytes(key,'utf-8'), DES.MODE_ECB)
        elif(mode == "CBC"):
            orig = DES.new(bytes(key,'utf-8'), DES.MODE_CBC)
        elif(mode == "CFB"):
            orig = DES.new(bytes(key,'utf-8'), DES.MODE_CFB)
        elif(mode == "CTR"):
            orig = DES.new(bytes(key,'utf-8'), DES.MODE_CTR)
    else:
        encrypted_message = socket.recv()
        msg = orig.decrypt(encrypted_message)
        print(msg.decode('utf-8'))
        
    