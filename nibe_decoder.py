import logging
from struct import unpack, pack

# Setup logger
logger = logging.getLogger('NIBE_DECODER')

# Global variables for special registers
reg28_value = None
reg29_value = None
reg30_value = None

def decode_register(reg, raw):
    """Decode a Nibe register value."""
    global reg28_value, reg29_value, reg30_value

    if len(raw) == 2:
        value = unpack('>H', raw)[0]
    else:
        value = unpack('B', raw)[0]

    if reg == 28:
        reg28_value = value
        return None
    elif reg == 29:
        reg29_value = value
        return None
    elif reg == 30:
        reg30_value = value
        interpret_operation_mode()
        return None

    if reg == 32:
        logger.debug(f"Register 32 (additional heating allowed) value: {value}")
        publish_mqtt("nibe/additional_heating_allowed", str(value))
        return None

    if reg == 31:
        logger.debug(f"Register 31 (heating status) value: {value}")
        if value == 1:
            publish_mqtt("nibe/heating_status", "auto")
        elif value == 3:
            publish_mqtt("nibe/heating_status", "lämmitys") #heating
        elif value == 5:
            publish_mqtt("nibe/heating_status", "lämminvesi") #domestic water
        elif value == 6:
            publish_mqtt("nibe/heating_status", "lisäys (sähkö)") #additional heating
        return None

    if reg in [1, 5, 6, 7, 12, 23, 11, 13, 14, 15, 16, 17, 18, 21]:
        return float(unpack('h', pack('H', value))[0] / 10)

    if reg in [0, 33, 34, 35, 36, 38, 44, 45, 46, 48, 100, 101, 102, 103, 104, 105]:
        return int(value)

    if reg in [4, 8]:
        return int(unpack('h', pack('H', value))[0] / 10)

    if reg == 25:
        return int(value / 10)

    if reg in [9, 10, 19, 20, 22, 24]:
        return float(value / 10)

    if reg in [40, 47]:
        return float(value / 2)

    if reg in [43, 49, 50]:
        return float(value)

    logger.warning(f"Register {reg} is not handled")
    return None

def interpret_operation_mode():
    """Interpret operation mode based on registers 28, 29, and 30."""
    from mqtt_helper import publish_mqtt

    if reg28_value == 0x0000 and reg29_value == 0x8222 and reg30_value == 0x0032:
        publish_mqtt("nibe/operation_mode", "Standby")
    elif reg28_value == 0x4409 and reg29_value == 0xA22A and reg30_value == 0x01FE:
        publish_mqtt("nibe/operation_mode", "Käyttövesi") #domestic water
    elif reg28_value == 0x0008 and reg29_value == 0xC22A and reg30_value == 0x000A:
        publish_mqtt("nibe/operation_mode", "Pois päältä") #power on, heatpump off
    elif reg28_value == 26634 and reg29_value == 49706 and reg30_value == 170:
        publish_mqtt("nibe/operation_mode", "Öljy paluu") #oil return
    elif reg28_value == 16394 and reg29_value == 49706 and reg30_value == 610:
        publish_mqtt ("nibe/operation_mode", "Lämmmitys") #heating
    elif reg28_value == 16394 and reg29_value == 49706 and reg30_value == 10:
        publish_mqtt ("nibe/operation_mode", "Lämmitys") #heating
    elif reg28_value == 0x0000 and reg29_value == 0xC22A and reg30_value == 0x003C:
        publish_mqtt("nibe/operation_mode", "Vain sähkövastukset") #additional heating only
    elif reg28_value == 16385 and reg29_value == 41514 and reg30_value == 50:
        publish_mqtt("nibe/operation_mode", "Käyttövesi") #domestic water
    elif reg28_value == 16393 and reg29_value == 49706 and reg30_value == 10:
        publish_mqtt("nibe/operation_mode", "Lämmitys") # heating
    elif reg28_value == 10 and reg29_value == 49706 and reg30_value == 10:
        publish_mqtt("nibe/operation_mode", "Pois päältä") #power on, heatpump off
    elif reg28_value == 28 and reg29_value == 49706 and reg30_value == 10:
        publish_mqtt("nibe/operation_mode", "lämmitys") #heating
    elif reg28_value == 10 and reg29_value == 49706 and reg30_value == 610:
        publish_mqtt("nibe/operation_mode", "Pois päältä") #power on, heatpump off
    elif reg28_value == 32776 and reg29_value == 49706 and reg30_value == 10:
        publish_mqtt("nibe/operation_mode", "Jäätymisensuoja") #freeze protection
    else:
        logger.warning(f"Unknown combination of register values: reg28={reg28_value}, reg29={reg29_value}, reg30={reg30_value}")
        publish_mqtt("nibe/operation_mode", f"Unknown mode: reg28={reg28_value}, reg29={reg29_value}, reg30={reg30_value}")
