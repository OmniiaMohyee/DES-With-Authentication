import zmq
from Crypto.Cipher import DES

context = zmq.Context()

#  Socket to talk to server
print("Receiver started..")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

request  = 0
print("Sending Alive Message")
socket.send(b"Receiver Alive~")

#  Get the reply.
message = socket.recv()


mode = message.decode("utf-8")
print("Received mode of operation: ",mode)

#DUMMY CODE TO DO DECRYPTION
orig = DES.new(bytes(key,'utf-8'), DES.MODE_ECB)
msg = orig.decrypt(encrypted_message)
print('here')
print(msg.decode('utf-8'))
    