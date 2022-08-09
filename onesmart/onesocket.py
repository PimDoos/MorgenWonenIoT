"""One Smart Control JSON-RPC Socket implementation"""
from hashlib import sha1
import json
from random import randint
import socket
import ssl
from const import *


class OneSocket:

	def __init__(self):
		# Initialize SSLContext without certificate checking
		self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
		self._ssl_context.check_hostname = False
		self._ssl_context.verify_mode = ssl.CERT_NONE

		# Allow old ciphers
		self._ssl_context.set_ciphers('DEFAULT')

		# Initialize caches
		self._response_cache = dict()
		self._event_cache = []

	def connect(self, host, port, username, password):
		username = username
		password_hash = sha1(password.encode()).hexdigest()
		self._raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._ssl_socket = self._ssl_context .wrap_socket(self._raw_socket)
		self._ssl_socket.connect((host, port))

		# Authenticate
		self.send_cmd(command=COMMAND_AUTHENTICATE, username=username, password=password_hash)

	def is_connected(self):
		if self._ssl_socket.get_channel_binding() == None:
			return False
		else:
			return True

	"""Start a new transaction"""
	def send_cmd(self, command, **kwargs):
		transaction_id = randint(1, MAX_TRANSACTION_ID)
		rpc_message = { RPC_COMMAND:command, RPC_TRANSACTION:transaction_id } | kwargs
		rpc_data = json.dumps(rpc_message) + "\r\n"
		print(rpc_message)
		self._ssl_socket.sendall(rpc_data.encode())

		return transaction_id
	
	def ping(self):
		self.send_cmd(command=COMMAND_PING)

	"""Fetch outstanding responses and cache them by transaction ID"""
	def get_responses(self):
		rpc_reply = self._ssl_socket.recv(SOCKET_BUFFER_SIZE)

		# One Smart splits messages over 1024 bytes. Sow them back together
		if(len(rpc_reply) == SOCKET_BUFFER_SIZE):
			rpc_reply += self._ssl_socket.recv(SOCKET_BUFFER_SIZE)
		
		reply = rpc_reply.decode()
		try:
			if(len(reply) > 8):
				reply_data = json.loads(reply)
				if not reply_data == None:
					if RPC_TRANSACTION in reply_data:
						# Received message is a transaction response
						transaction_id = reply_data[RPC_TRANSACTION]
						self._response_cache[transaction_id] = reply_data
					else:
						# Message is not part of a transaction. Add to queue.
						self._event_cache.append(reply_data)
		except json.JSONDecodeError:
			print("Decoding JSON failed for {}".format(reply))
		except:
			print("Unexpected error while loading responses")

	"""Get the result of a cached transaction"""
	def get_transaction(self, transaction_id):
		return self._response_cache.get(transaction_id, None)
	
	"""Return events and clear the cache"""
	def get_events(self):
		events = self._event_cache
		self._event_cache = []
		return events

