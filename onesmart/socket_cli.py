"""Boilerplate script to provide CLI access to One Smart Control"""
from re import match
from time import time
from const import *
from onesmartsocket import OneSmartSocket

gateway = OneSmartSocket()
gateway.connect("oneserver.local", 9010)
login_transaction = gateway.authenticate("username", "password")
gateway.get_transaction(login_transaction)

last_ping = time()
meters = None
site = None

def command_wait(command, **kwargs):
	transaction_id = gateway.send_cmd(command, **kwargs)
	transaction_done = False
	while not transaction_done:
		gateway.get_responses()
		transaction = gateway.get_transaction(transaction_id)
		transaction_done = transaction != None

	return transaction
