The ventilation unit is a Zehnder StorkAir WHR930 Luxe balanced ventilation unit. Underneath the top cover you will find a cirquit board with 1 RS485 connection (in use by the monitoring box) and two RS232 connections (DB9 and RJ45).
You can connect these to Home Assistant via MQTT by using this script: [adorobis/hacomfoairmqtt](https://github.com/adorobis/hacomfoairmqtt)

Additionally, you will find some additional template sensors for various useful data points, such as:
- CO2 sensors (connected via Analog inputs)
- Airflow calculations (approximated based on fan speeds and specification)
- Thermal flow (approximated)
- Temperature deltas

