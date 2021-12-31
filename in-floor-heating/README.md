The in-floor heating is fed by the heatpump through a central splitter in the service closet in the attic. The valves on the splitter use a standard screwhead. By hooking up TRV motors in combination with temperature sensors per room, you can achieve per-room temperature control (to a degree, ha-ha).

I used 3V TRV motors harvested from Sygonix BLE thermostats, controlled by an ESP8266 running ESPHome. You can also use 230V radiator motors in combination with a suitable relay board.


Files
=====
`climate-trv.yaml` contains generic thermostat entries to control the valves for the in-floor heating.
