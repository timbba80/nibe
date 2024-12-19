import logging
import time
from mqtt_handler import publish_availability, publish_discovery_payloads
from serial_handler import setup_serial_connection
from decoder import decode_register

logger = logging.getLogger('NIBE')

nibe_registers = {
    # Add register mapping based on the original script
}

mqtt_discovery_sensors = {
    # Add discovery sensor configurations based on the original script
}

def run():
    logger.info("Starting the main loop...")
    publish_availability("online")
    publish_discovery_payloads(mqtt_discovery_sensors)
    
    ser = setup_serial_connection()
    if not ser:
        return

    try:
        while True:
            try:
                if ser.read(1)[0] != 0x03:
                    logger.debug("No start byte found")
                    continue
                logger.debug("Start byte found, reading data...")
                ret = ser.read(2)
                if ret[0] != 0x00 or ret[1] != 0x14:
                    logger.debug("Invalid start frame")
                    continue
                ser.write(b"\x06")
                frm = ser.read(4)
                if frm[0] == 0x03:
                    continue
                l = int(frm[3])
                frm += ser.read(l + 1)
                ser.write(b"\x06")
                crc = 0
                for i in frm[:-1]:
                    crc ^= i
                if crc != frm[-1]:
                    logger.warning("Frame CRC error")
                    continue
                msg = frm[4:-1]
                l = len(msg)
                i = 4
                while i <= l:
                    reg = msg[i - 3]
                    if i != l and (msg[i] == 0x00 or i == (l - 1)):
                        raw = bytes([msg[i - 2], msg[i - 1]])
                        i += 4
                    else:
                        raw = bytes([msg[i - 2]])
                        i += 3
                    if reg in nibe_registers:
                        value = decode_register(reg, raw)
                        if value is not None:
                            mqtt_topic = nibe_registers[reg]
                            publish_mqtt(mqtt_topic, value)
            except Exception as e:
                logger.warning(f"Error in Nibe data processing: {e}")
                time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Script interrupted, shutting down...")
    finally:
        publish_availability("offline")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    logger.info("Starting Nibe heat pump MQTT bridge")
    run()
