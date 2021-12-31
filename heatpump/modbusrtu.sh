#!/bin/bash
# Simple listener to connect a USB Serial converter to a TCP socket.
while :
do
        echo "Starting listener"
        stty -F /dev/ttyUSB0 9600 raw -echo -echoe -echok
        /bin/nc -l 501 </dev/ttyUSB0 >/dev/ttyUSB0
        echo "Client disconnected."
done
