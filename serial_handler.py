import logging
import time
import serial
from nibe_decoder import decode_register
from mqtt_helper import publish_mqtt
from constants import nibe_registers

logger = logging.getLogger('NIBE_SERIAL')
logger.info(f"publish_mqtt is imported and callable: {callable(publish_mqtt)}")

serial_port = "/dev/ttyUSB0"
ser = serial.Serial(serial_port, 19200, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, timeout=3)

def process_serial_data():
    logger.info("Starting serial data processing...")
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
                        logger.debug(f"Preparing to publish: topic={mqtt_topic}, value={value}")
                        publish_mqtt(mqtt_topic, value)
                        logger.debug(f"Published to MQTT: topic={mqtt_topic}, value={value}")
        except Exception as e:
            logger.warning(f"Error in serial data processing: {e}")
            time.sleep(1)