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
    if reg in [31, 32, 1, 5, 6, 7, 12, 23, 11, 13, 14, 15, 16, 17, 18, 21, 0, 33, 34, 35, 36, 38, 44, 45, 46, 48, 100, 101, 102, 103, 104, 105, 4, 8, 25, 9, 10, 19, 20, 22, 24, 40, 47, 43, 49, 50]:
        handle_known_registers(reg, value)
    else:
        logger.warning(f"Register {reg} is not handled")
    return None

def interpret_state():
    if reg28_value == 0x0000 and reg29_value == 0x8222 and reg30_value == 0x0032:
        publish_mqtt("nibe/operation_mode", "Standby")
    # Add more interpretations based on the original script
    else:
        logger.warning(f"Unknown combination of register values: reg28={reg28_value}, reg29={reg29_value}, reg30={reg30_value}")
        publish_mqtt("nibe/operation_mode", f"Unknown mode: reg28={reg28_value}, reg29={reg29_value}, reg30={reg30_value}")

def handle_known_registers(reg, value):
    if reg == 31:
        if value == 1:
            publish_mqtt("nibe/heating_status", "auto")
        elif value == 3:
            publish_mqtt("nibe/heating_status", "lämmitys")
        elif value == 5:
            publish_mqtt("nibe/heating_status", "lämminvesi")
        elif value == 6:
            publish_mqtt("nibe/heating_status", "lisäys (sähkö)")
    elif reg == 32:
        publish_mqtt("nibe/additional_heating_allowed", str(value))
    else:
        publish_mqtt("nibe/other_register", str(value))
