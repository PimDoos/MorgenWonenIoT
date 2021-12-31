Configuration to connect the Mitsubishi Ecodan EHST20D-VM2C to Home Assistant.

Files
=====
The `modbus-usb.yaml` and `modbus-tcp.yaml` files contain the connection settings for the ModBus connection. Choose `modbus-usb.yaml` when using a direct local USB connection, `modbus-tcp.yaml` when the modbus is connected to a remote device.

The other modbus yaml files contain registers for sensors, switches, climate and binary sensors.
The `template_ehst20d.yaml` file contains templates to convert some data from the ModBus to strings.

Physical connection
===================
The heatpump is equipped with a Procon MelcoBEMS Mini A1M ([installer manual](https://library.mitsubishielectric.co.uk/pdf/book/MELCOBEMS_Mini_A1M_Install_User_Manual)), which exposes the heatpump's parameters over ModBus to the One Smart Control monitoring box.
We can use Home Assistant's ModBus integration to read data from this ModBus. Please note: this requires disconnecting it from the One Smart Control box and as such, the monitoring portal will no longer show current data from your heatpump.

Since ModBus is using the RS485 specification, we have a few options to connect it to Home Assistant:
- Use a RS485 to USB converter. You can either plug this in directly to your machine running Home Assistant or use the `modbusrtu.service` systemd file to expose it as a ModBus RTU over TCP port.
- Use a RS485 to Ethernet converter. This exposes the ModBus as a ModBus RTU over TCP port in your network.

ModBus settings
===============

Address
-------

In a ModBus network, every device has each own address. You can find the address by looking adding together the value of the DIP switches on the Procon module. The minimum value is 1.
| Switch number | Value when on |
| --------------|---------------|
| 1 | 1 |
| 2 | 2 |
| 3 | 4 |
| 4 | 8 |
| 5 | 16 |


Registers
---------
Every value exposed by the heatpump is assigned a ModBus register. Mitsubishi has provided tables for these values [here](https://library.mitsubishielectric.co.uk/pdf/book/MELCOBEMS_MINI__A1M__ATW_Modbus_Register_Tables.pdf).
To see if a register is available on this unit, look at the __FTC5__ column.
