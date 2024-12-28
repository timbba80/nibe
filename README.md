Simple python script for being able to read data from older Nibe/Mitsubishi hydrolution split air to water heatpumps which do not have official data bus (modbus, wifi, Ethernet) for collecting data. 

It utilizes logger (menu 9.3.2) for reading the data. 

Working at least with Mitsubishi Heavy Industries hydrolution HMA100v and Nibe ACVM270. 
Other MHI/Nibe split pumps might work as well, as long as they use the same logic for the logger function (handshake between the heatpump and the system to which the RS485 adapter is connected to (and from where the python script is ran from) and as long as they have same registers than the two earlier mentioned models.

Big thanks to CTR49 for the registers (register.txt and register.html), source: https://github.com/ctr49/nibe-knx-gw. 
Note! The registers most likely vary basis of the model of the air to water heatpump and to Eddso (https://knx-user-forum.de/forum/öffentlicher-bereich/knx-eib-forum/20371-anbindung-modbus-nibe?p=650159#post650159) for the initial python script. Script has been modified with openai chatpt e.g. for including mqtt.

The register for operation mode is still incomplete, which results to "unknown" status in certain situations in the operation mode. There are also some registers which are not recognized. They send data but what the data inteprets (which sensor) is unknown.

The sensor names in nibe.py are basis of the original python script. I've kept them as they are and am using Home Assistant sensor entity to customise them. As most likely the usage of this script will be so minor, I do not see point of adjusting these nor modifying the script to add support for automatic translation. Feel free to modify... in theory the sensor data could be in sensor.py file, mqtt in own file, decoding in own file and translation in own file etc....


**Requirements: 
**
paho mqtt client
RS-485 module. 
MQTT broker
Python

**Installation: 
**


RS-485 setup:

1. You need a cable which has RJ-45 plug at the other end.
2. The other end needs to be connected to RS-485 adapter as follows: Pin 1 D-, Pin 2 D+. Leave other wires as is (do not connect), only the data + and data - are required. NOTE! connecting other wires or connecting them incorrectly might lead to breaking the heatpump, thus be sure to connect the correct wires! Source: https://knx-user-forum.de/forum/öffentlicher-bereich/knx-eib-forum/20371-anbindung-modbus-nibe?p=518225#post518225)
3. The cable is connected either to a RJ-45 socket in the "motherboard" of the heat pump (can be seen after removing the front panel) or to the connector behind the display panel (I haven't tested the display panel connection, thus not sure if it works). 

Python script: 

4. Change COM port in nibe.py to the correct COM port (row 28)
5. Configure MQTT details in nibe.py (row 15, 16)

Heat pump configuration:

6. Once RS-485 cable has been set up and connected, go to menu option 9.3.2 (logger) in the heat pump and enable logger. Note! For accessing menu 9.3.2 one might need to change menu type to "service" from 8.1.1).

Host system from where the nibe.py is ran from: 

8. Start the script (e.g. python nibe.py or python3 nibe.py). You should see data being received by the mqtt broker now. If you have enabled logging to console (nibe.py row 8), basis of the level defined (debug, info, warning....) you will see the log info in the terminal screen. 
