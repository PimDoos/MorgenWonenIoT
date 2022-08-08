import json
import socket
import ssl
from hashlib import sha1
from time import sleep
from token import NEWLINE

# Configuration
one_host = "127.0.0.1" # IP of One Smart Control 'Connect' box
one_port = 9010 # TCP Port running the TLS socket
one_user = "something" # App Username
one_password = "somethingsecret" # App Password

password_hash = sha1(one_password.encode()).hexdigest()

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
ssl_context.set_ciphers('DEFAULT')


raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

transaction_id = 10
with ssl_context.wrap_socket(raw_socket) as ssl_socket:
	ssl_socket.connect((one_host, one_port))
	
	command = {"cmd":"authenticate","username":one_user, "password": password_hash, "transaction": 10}
	rpc_data = json.dumps(command) + "\r\n"
	print(command)
	ssl_socket.sendall(rpc_data.encode())

	transaction_id += 1
  
  # Subscribe to all events
	command = {"cmd":"events","action":"subscribe","topics":["SITE","AUTHENTICATION","DEVICE","ROOM","METER","PRESET","PRESETGROUP","TRIGGER","ROLE","USER","SITEPRESET","UPGRADE","MESSAGE","ENERGY"], "transaction": transaction_id}
	rpc_data = json.dumps(command) + "\r\n"
	print(command)
	ssl_socket.send(rpc_data.encode())

  # Listen and wait
	while True:
		rpc_reply = ssl_socket.recv(1024)
		reply = rpc_reply.decode()
		if(len(reply) > 16):
			reply_data = json.loads(reply)
			print(reply)

		
