import logging
from struct import unpack, pack
from mqtt_handler import publish_mqtt

logger = logging.getLogger('NIBE')

reg28_value = None
reg29_value = None
reg30_value = None

def decode_register(reg, raw):
    global reg28_value, reg29_value, reg30_value
    if len(raw) == 2:
        value = unpack('>H', raw)[0]
    else:
        value = unpack('B', raw)[0]
    
    # Handle registers 28, 29, and 30
    if reg == 28:
        reg28_value = value
        logger.debug(f"Register 28 (operation mode) value: {reg28_value}")
        return None
    elif reg == 29:
        reg29_value = value
        logger.debug(f"Register 29 (operation mode) value: {reg29_value}")
        return None
    elif reg == 30:
        reg30_value = value
        logger.debug(f"Register 30 (operation mode) value: {reg30_value}")
        interpret_state()
        return None

    # Handle additional cases for other registers...
    # Add more decoding logic based on the original script

    logger.warning(f"Register {reg} is not handled")
    return None

def interpret_state():
    if reg28_value == 0x0000 and reg29_value == 0x8222 and reg30_value == 0x0032:
        publish_mqtt("nibe/operation_mode", "Standby")
    # Add more interpretations based on the original script
    else:
        logger.warning(f"Unknown combination of register values: reg28={reg28_value}, reg29={reg29_value}, reg30={reg30_value}")
        publish_mqtt("nibe/operation_mode", f"Unknown mode: reg28={reg28_value}, reg29={reg29_value}, reg30={reg30_value}")
