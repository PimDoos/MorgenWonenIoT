from time import time
from const import *
from onesocket import OneSocket

gateway = OneSocket()
gateway.connect("127.0.0.1", 9010, "appusername", "apppassword")
transaction_events = gateway.send_cmd(command=COMMAND_EVENTS, action=ACTION_SUBSCRIBE, topics=["SITE","AUTHENTICATION","DEVICE","ROOM","METER","PRESET","PRESETGROUP","TRIGGER","ROLE","USER","SITEPRESET","UPGRADE","MESSAGE","ENERGY"])
transaction_meters = gateway.send_cmd(command=COMMAND_METER, action=ACTION_LIST)

last_ping = time()
meters = None
while gateway.is_connected():
	# Read outstanding responses
	gateway.get_responses()

	# Keep the connection alive
	if time() - last_ping > PING_INTERVAL:
		gateway.ping()
		last_ping = time()
	
	if not meters:
		transaction = gateway.get_transaction(transaction_meters)
		print(transaction)
		if transaction != None:
			result_meters = transaction[RPC_RESULT]["meters"]
			meters = dict()
			for meter in result_meters:
				meters[meter["id"]] = meter
			print(meters)
	
	events = gateway.get_events()
	if len(events) > 0:
		for event in events:
			if event[RPC_EVENT] == EVENT_ENERGY_CONSUMPTION and meters != None:
				print()
				print("=== ENERGY READING ===")
				for reading in event[RPC_DATA][RPC_VALUES]:
					meter_name = meters[reading["id"]]["name"]
					meter_value = reading["value"]
					print("{name}: {value} W".format(name=meter_name,value=meter_value))
				
				print("======================")
