import logging
import serial

logger = logging.getLogger('NIBE')

def setup_serial_connection(port="/dev/ttyUSB0", baudrate=19200):
    try:
        ser = serial.Serial(port, baudrate, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, timeout=3)
        logger.debug("Serial port opened successfully")
        return ser
    except serial.SerialException as e:
        logger.error(f"Failed to open serial port: {e}")
        return None
