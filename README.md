Simple python script for being able to read data from older Nibe/Mitsubishi hydrolution split air to water heatpumps which do not have official data bus (modbus, wifi, Ethernet) for collecting data. 

It utilizes the connection bus for Nibe/MHI RE10 room unit. 

Requirements: 

paho mqtt client
RS-485 module. 
MQTT broker
Python

Big thanks for CTR49 for the registers (register.txt and register.html), source: https://github.com/ctr49/nibe-knx-gw. 
Note! The registers most likely vary basis of the model of the air to water heatpump. 
Note! The register for operation mode is still incomplete, which results to "unknown" status in certain situations in the operation mode. I have not yed had the time to check from the heatpump what is the actual state for unknown states. Will do it later on. 

Also big thanks for Eddso (https://knx-user-forum.de/forum/öffentlicher-bereich/knx-eib-forum/20371-anbindung-modbus-nibe?p=650159#post650159) for the initial python script. Script has been modified with openai chatpt e.g. for including mqtt. 


Installation: 



RS-485 setup:

1. You need a cable which has RJ-45 plug at the other end.
2. The other end needs to be connected to RS-485 adapter as follows: Pin 1 D-, Pin 2 D+. Leave other wires as is (do not connect), only the data + and data - are required. NOTE! connecting other wires or connecting them incorrectly might lead to breaking the heatpump board, thus be sure to connect the correct wires! Source: https://knx-user-forum.de/forum/öffentlicher-bereich/knx-eib-forum/20371-anbindung-modbus-nibe?p=518225#post518225)
3. The cable is connected either to a RJ-45 socket in the "motherboard" of the heat pump (can be seen after removing the front panel). In certain models the connector might be behind the display (open front panel, open the display screws and the connector is behind the display board).

Python script: 
4. Change COM port in nibe.py to the correct COM port (row 28)
5. Configure MQTT details in nibe.py (row 14, 15)

Heat pump configuration:

6. Once RS-485 cable has been set up and connected, go to menu option 9.3.2 (logger) in the heat pump and enable logger. Note! For accessing menu 9.3.2 one might need to change menu type to "service" from 8.1.1).

Server from where the nibe.py is ran from: 

8. Start the script (e.g. python nibe.py or python3 nibe.py)

If you have enabled logging to console (nibe.py row 8), basis of the logger level you will see in the terminal information (e.g. if logger level = warning, you will see if something is failing, info and debug will give you more data). You should be able to see data also now in the mqtt broker, and in mqtt explorer (if you use one). 
