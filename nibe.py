from mqtt_helper import publish_availability, publish_discovery_payloads, mqtt_client
from serial_handler import process_serial_data
import logging

# Setup logger
#logging.basicConfig(level=logging.WARNING)
logging.basicConfig(level=logging.ERROR, filename='nibe_debug.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('NIBE')

def main():
    logger.info("Starting the Nibe MQTT bridge")
    try:
        # Publish the device's availability as online
        publish_availability("online")
        
        # Publish Home Assistant discovery payloads
        publish_discovery_payloads()
        
        # Start processing serial data
        process_serial_data()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        # Publish availability as offline before exiting
        publish_availability("offline")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    main()
