import logging
import serial
import time
import paho.mqtt.client as mqtt
from struct import unpack, pack

# Setup logger
logging.basicConfig(level=logging.WARNING) #change logging level as wanted. This will log messages to console. If you want to use text file, use the logging configuration from below. 
#logging.basicConfig(level=logging.WARNING, filename='nibe_debug.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('NIBE')

# MQTT setup
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(username="username", password="password")  #add MQTT username + password
mqtt_client.connect("mqtt server", 1883, 60) #add MQTT server IP /DNS name. Change port if required1883


def publish_mqtt(topic, message):
    mqtt_client.publish(topic, message)
    logger.info(f"Published {message} to {topic}")

# Publish "online" status to availability topic
def publish_availability(status):
    mqtt_client.publish("nibe/status", status)
    logger.info(f"Published availability status: {status}")

# Serial connection to Nibe heat pump (adjust COM port for Windows)
serial_port = "/dev/ttyUSB0"  # Adjust to your correct COM port
ser = serial.Serial(serial_port, 19200, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, timeout=3)

logger.debug("Serial port opened successfully")

# Register mapping, expanded to match original script
nibe_registers = {
    0: "nibe/cpu_id",
    1: "nibe/outdoor_temp_c",  
    4: "nibe/heating_curve",
    5: "nibe/flow_setpoint_c",  
    6: "nibe/flow_actual_c",  
    7: "nibe/return_temp_c",
    8: "nibe/degree_minutes",
    12: "nibe/domestic_hot_water_top_temp",
    25: "nibe/compressor_starts",
    31: "nibe/heating_status",
    32: "nibe/additional_heating_allowed",
    33: "nibe/max_df_compressor",
    34: "nibe/verd_freq_reg_p",
    35: "nibe/min_start_time_freq_min",
    36: "nibe/min_time_const_freq_min",
    38: "nibe/comp_freq_grad_min",
    44: "nibe/pump_speed_percent",
    45: "nibe/bw_reg_p",
    46: "nibe/bw_reg_q",
    48: "nibe/bw_reg_value_xp_percent",
    100: "nibe/date_year",
    101: "nibe/date_month",
    102: "nibe/date_day",
    103: "nibe/time_hour",
    104: "nibe/time_minute",
    105: "nibe/time_second",
    24: "nibe/run_time_compressor_h",
    9: "nibe/comp_freq_desired_hz",
    10: "nibe/comp_freq_actual_hz",
    19: "nibe/high_pressure_bar",
    20: "nibe/low_pressure_bar",
    22: "nibe/ams_phase_is_a",
    40: "nibe/hysteresis",
    47: "nibe/bw_reg_xp",
    43: "nibe/stop_temp_heating_c",
    49: "nibe/domestic_hot_water_start_temp",
    50: "nibe/domestic_hot_water_stop_temp",
    28: "nibe/operation_mode_reg_28",
    29: "nibe/operation_mode_reg_29",
    30: "nibe/operation_mode_reg_30",
    23: "nibe/inverter_temp_tho_ip",
    11: "nibe/condenser_off_max",  # Condenser off (MAX)
    13: "nibe/domestic_hot_water_bottom",  # Domestic hot water bottom
    14: "nibe/tho_r1_evap_temp",  # Tho-R1 evaporator temp
    15: "nibe/tho_r2_evap_temp",  # Tho-R2 evaporator temp
    16: "nibe/suction_gas_temp_tho_s",  # Suction gas temp. Tho-S
    17: "nibe/hot_gas_temp_tho_d",  # Hot gas temp. Tho-D
    18: "nibe/liquid_temp_ams",  # Liquid temp. AMS
    21: "nibe/resp_at_ams_tho_a",  # Response at AMS Tho-A
}
  
# uudet 28 eteenpäin


# Define unique IDs and MQTT discovery configurations for each sensor
mqtt_discovery_sensors = {
    "nibe/pump_speed_percent": {
        "name": "Pump Speed Percent",
        "unit_of_measurement": "%",
        "state_topic": "nibe/pump_speed_percent",
        "unique_id": "nibe_pump_speed_percent"
    },
#    "nibe/cpu_id": {
#        "name": "CPU ID",
#        "state_topic": "nibe/cpu_id",
#        "unique_id": "nibe_cpu_id"
#    },
#uudet alkaa tästä
    "nibe/inverter_temp_tho_ip": {
        "name": "Inverter temp Tho-IP",
        "state_class": "measurement",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "state_topic": "nibe/inverter_temp_tho_ip",
        "unique_id": "nibe_inverter_temp_tho_ip"
    },
    "nibe/operation_mode": {
        "name": "Nibe Operation Mode",
        "state_topic": "nibe/operation_mode",
    "unique_id": "nibe_operation_mode"
    },
    "nibe/condenser_off_max": {
        "name": "Condenser Off (MAX)",
        "state_topic": "nibe/condenser_off_max",
        "unit_of_measurement": "°C",  # Adjust if needed
        "device_class": "temperature",
        "unique_id": "nibe_condenser_off_max"
    },
    "nibe/domestic_hot_water_bottom": {
        "name": "Domestic Hot Water Bottom",
        "state_topic": "nibe/domestic_hot_water_bottom",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "unique_id": "nibe_domestic_hot_water_bottom"
    },
    "nibe/tho_r1_evap_temp": {
        "name": "Tho-R1 Evaporator Temp",
        "state_topic": "nibe/tho_r1_evap_temp",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "unique_id": "nibe_tho_r1_evap_temp"
    },
    "nibe/tho_r2_evap_temp": {
        "name": "Tho-R2 Evaporator Temp",
        "state_topic": "nibe/tho_r2_evap_temp",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "unique_id": "nibe_tho_r2_evap_temp"
    },
    "nibe/suction_gas_temp_tho_s": {
        "name": "Suction Gas Temp Tho-S",
        "state_topic": "nibe/suction_gas_temp_tho_s",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "unique_id": "nibe_suction_gas_temp_tho_s"
    },
    "nibe/hot_gas_temp_tho_d": {
        "name": "Hot Gas Temp Tho-D",
        "state_topic": "nibe/hot_gas_temp_tho_d",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "unique_id": "nibe_hot_gas_temp_tho_d"
    },
    "nibe/liquid_temp_ams": {
        "name": "Liquid Temp AMS",
        "state_topic": "nibe/liquid_temp_ams",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "unique_id": "nibe_liquid_temp_ams"
    },
    "nibe/resp_at_ams_tho_a": {
        "name": "Response at AMS Tho-A",
        "state_topic": "nibe/resp_at_ams_tho_a",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "unique_id": "nibe_resp_at_ams_tho_a"
    },     
#uudet loppuu tähän  
    "nibe/heating_curve": {
        "name": "Heating Curve",
        "state_topic": "nibe/heating_curve",
        "state_class": "measurement",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_heating_curve"
    },
    "nibe/return_temp_c": {
        "name": "Return Temperature",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "state_topic": "nibe/return_temp_c",
        "unique_id": "nibe_return_temp_c"
    },
    "nibe/degree_minutes": {
        "name": "Degree Minutes",
        "state_topic": "nibe/degree_minutes",
        "state_class": "measurement",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_degree_minutes"
    },
    "nibe/domestic_hot_water_top_temp": {
        "name": "Domestic Hot Water Top Temperature",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "state_topic": "nibe/domestic_hot_water_top_temp",
        "unique_id": "nibe_domestic_hot_water_top_temp"
    },
    "nibe/max_df_compressor": {
        "name": "Max DF Compressor",
        "state_topic": "nibe/max_df_compressor",
        "unit_of_measurement": "Hz",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_max_df_compressor"
    },
    "nibe/verd_freq_reg_p": {
        "name": "Verd Freq Reg P",
        "state_topic": "nibe/verd_freq_reg_p",
        "unit_of_measurement": "Hz",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_verd_freq_reg_p"
    },
    "nibe/min_start_time_freq_min": {
        "name": "Min Start Time Freq Min",
        "unit_of_measurement": "Hz",
        "state_topic": "nibe/min_start_time_freq_min",
        "unique_id": "nibe_min_start_time_freq_min"
    },
    "nibe/min_time_const_freq_min": {
        "name": "Min Time Const Freq Min",
        "state_topic": "nibe/min_time_const_freq_min",
        "unit_of_measurement": "Hz",
        "unique_id": "nibe_min_time_const_freq_min"
    },
    "nibe/comp_freq_grad_min": {
        "name": "Comp Freq Grad Min",
        "state_topic": "nibe/comp_freq_grad_min",
        "unit_of_measurement": "Hz",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_comp_freq_grad_min"
    },
    "nibe/bw_reg_p": {
        "name": "BW Reg P",
        "state_topic": "nibe/bw_reg_p",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_bw_reg_p"
    },
    "nibe/bw_reg_q": {
        "name": "BW Reg Q",
        "state_topic": "nibe/bw_reg_q",
        "value_template": "{{ value | float }}",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "unique_id": "nibe_bw_reg_q"
    },
    "nibe/bw_reg_value_xp_percent": {
        "name": "BW Reg Value XP Percent",
        "unit_of_measurement": "%",
        "state_topic": "nibe/bw_reg_value_xp_percent",
        "unique_id": "nibe_bw_reg_value_xp_percent"
    },
#    "nibe/date_year": {
#        "name": "Date Year",
#        "state_topic": "nibe/date_year",
#        "unique_id": "nibe_date_year"
#    },
#    "nibe/date_month": {
#        "name": "Date Month",
#        "state_topic": "nibe/date_month",
#        "unique_id": "nibe_date_month"
#    },
#    "nibe/date_day": {
#        "name": "Date Day",
#        "state_topic": "nibe/date_day",
#        "unique_id": "nibe_date_day"
#    },
#    "nibe/time_hour": {
#        "name": "Time Hour",
#        "state_topic": "nibe/time_hour",
#        "unique_id": "nibe_time_hour"
#    },
#    "nibe/time_minute": {
#        "name": "Time Minute",
#        "state_topic": "nibe/time_minute",
#        "unique_id": "nibe_time_minute"
#    },
#    "nibe/time_second": {
#        "name": "Time Second",
#        "state_topic": "nibe/time_second",
#        "unique_id": "nibe_time_second"
#    },
    "nibe/run_time_compressor_h": {
        "name": "Run Time Compressor Hours",
        "state_topic": "nibe/run_time_compressor_h",
        "device_class": "duration",
        "unit_of_measurement": "h",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_run_time_compressor_h"
    },
    "nibe/comp_freq_desired_hz": {
        "name": "Comp Freq Desired Hz",
        "unit_of_measurement": "Hz",
        "state_topic": "nibe/comp_freq_desired_hz",
        "unique_id": "nibe_comp_freq_desired_hz"
    },
    "nibe/comp_freq_actual_hz": {
        "name": "Comp Freq Actual Hz",
        "unit_of_measurement": "Hz",
        "state_topic": "nibe/comp_freq_actual_hz",
        "unique_id": "nibe_comp_freq_actual_hz"
    },
    "nibe/high_pressure_bar": {
        "name": "High Pressure Bar",
        "unit_of_measurement": "bar",
        "state_topic": "nibe/high_pressure_bar",
        "unique_id": "nibe_high_pressure_bar"
    },
    "nibe/low_pressure_bar": {
        "name": "Low Pressure Bar",
        "unit_of_measurement": "bar",
        "state_topic": "nibe/low_pressure_bar",
        "unique_id": "nibe_low_pressure_bar"
    },
    "nibe/ams_phase_is_a": {
        "name": "AMS Phase Current",
        "unit_of_measurement": "A",
        "state_topic": "nibe/ams_phase_is_a",
        "unique_id": "nibe_ams_phase_is_a"
    },
    "nibe/hysteresis": {
        "name": "Hysteresis",
        "state_topic": "nibe/hysteresis",
        "state_class": "measurement",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_hysteresis"
    },
    "nibe/bw_reg_xp": {
        "name": "BW Reg XP",
        "state_topic": "nibe/bw_reg_xp",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_bw_reg_xp"
    },
    "nibe/stop_temp_heating_c": {
        "name": "Stop Temp Heating",
        "unit_of_measurement": "°C",
        "state_topic": "nibe/stop_temp_heating_c",
        "unique_id": "nibe_stop_temp_heating_c"
    },
    "nibe/domestic_hot_water_start_temp": {
        "name": "Domestic Hot Water Start Temp",
        "unit_of_measurement": "°C",
        "state_topic": "nibe/domestic_hot_water_start_temp",
        "unique_id": "nibe_domestic_hot_water_start_temp"
    },
    "nibe/domestic_hot_water_stop_temp": {
        "name": "Domestic Hot Water Stop Temp",
        "unit_of_measurement": "°C",
        "state_topic": "nibe/domestic_hot_water_stop_temp",
        "unique_id": "nibe_domestic_hot_water_stop_temp"
    },
    "nibe/outdoor_temp_c": {
        "name": "Outdoor Temperature",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "state_topic": "nibe/outdoor_temp_c",
        "unique_id": "nibe_outdoor_temp_c"
    },
    "nibe/flow_setpoint_c": {
        "name": "Flow Setpoint Temperature",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "state_topic": "nibe/flow_setpoint_c",
        "unique_id": "nibe_flow_setpoint_c"
    },
    "nibe/flow_actual_c": {
        "name": "Flow Actual Temperature",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "state_topic": "nibe/flow_actual_c",
        "unique_id": "nibe_flow_actual_c"
    },
    "nibe/compressor_starts": {
        "name": "Compressor starts",
        "state_topic": "nibe/compressor_starts",
        "unit_of_measurement": "x",
        "state_class": "total_increasing",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_compressor_starts"
    },
    "nibe/heating_status": {
        "name": "Heating Status",
        "state_topic": "nibe/heating_status",
        "unique_id": "nibe_heating_status"
        # No unit_of_measurement or device_class needed here
    },
    "nibe/additional_heating": {
        "name": "Additional Heating Allowed",
        "state_topic": "nibe/additional_heating_allowed",
        "unique_id": "nibe_additional_heating_allowed",
        "value_template": "{{ value | int }}",  # Ensure Home Assistant interprets 0 and 1 as integers
        "availability_topic": "nibe/status",
        "payload_available": "online",
        "payload_not_available": "offline",
        "device": {
            "identifiers": ["nibe_heat_pump"],
            "name": "Nibe Heat Pump",
            "manufacturer": "Nibe",
            "model": "EasySolar",
            "sw_version": "1.0"
    }
},

}


# Publish MQTT discovery payload for each sensor
def publish_discovery_payloads():
    for sensor, config in mqtt_discovery_sensors.items():
        discovery_topic = f"homeassistant/sensor/{config['unique_id']}/config"
        
        # Build the base payload
        payload = {
            "name": config["name"],
            "state_topic": config["state_topic"],
            "unique_id": config["unique_id"],
            "availability_topic": "nibe/status",
            "payload_available": "online",
            "payload_not_available": "offline",
            "device": {
                "identifiers": ["nibe_heat_pump"],
                "name": "Nibe Heat Pump",
                "manufacturer": "Nibe",
                "model": "EasySolar",
                "sw_version": "1.0"
            }
        }

        # Add optional fields only if they exist
        if config.get("unit_of_measurement"):
            payload["unit_of_measurement"] = config["unit_of_measurement"]
        if config.get("device_class"):
            payload["device_class"] = config["device_class"]
        if config.get("value_template"):
            payload["value_template"] = config["value_template"]

        # Publish the discovery payload as JSON
        mqtt_client.publish(discovery_topic, str(payload).replace("'", '"'), qos=0, retain=True)
        logger.info(f"Published MQTT discovery payload for {config['name']}")

# Initialize global variables to store register 28, 29, and 30 values
reg28_value = None
reg29_value = None
reg30_value = None

def _decode(reg, raw):
    global reg28_value, reg29_value, reg30_value  # Ensure these variables are accessible
    
    if len(raw) == 2:
        value = unpack('>H', raw)[0]
    else:
        value = unpack('B', raw)[0]

    # Handle registers 28, 29, and 30
    if reg == 28:
        reg28_value = value
        logger.debug(f"Register 28 (operation mode) value: {reg28_value}")
        return None  # Avoid falling through to unhandled case
    elif reg == 29:
        reg29_value = value
        logger.debug(f"Register 29 (operation mode) value: {reg29_value}")
        return None  # Avoid falling through to unhandled case
    elif reg == 30:
        reg30_value = value
        logger.debug(f"Register 30 (operation mode) value: {reg30_value}")

        # Now that we have all three registers, interpret the state
        if reg28_value == 0x0000 and reg29_value == 0x8222 and reg30_value == 0x0032:
            publish_mqtt("nibe/operation_mode", "Standby")
        elif reg28_value == 0x4409 and reg29_value == 0xA22A and reg30_value == 0x01FE:
            publish_mqtt("nibe/operation_mode", "Domestic Hot Water Preparation")
        elif reg28_value == 0x0008 and reg29_value == 0xC22A and reg30_value == 0x000A:
            publish_mqtt("nibe/operation_mode", "Heating Pump On, AMS Off")
        elif reg28_value == 0x0000 and reg29_value == 0xC22A and reg30_value == 0x003C:
            publish_mqtt("nibe/operation_mode", "Auxiliary Heating On")
        elif reg28_value == 16385 and reg29_value == 41514 and reg30_value == 50:
            publish_mqtt("nibe/operation_mode", "Heating Domestic Water")
        elif reg28_value == 16393 and reg29_value == 49706 and reg30_value == 10:
            publish_mqtt("nibe/operation_mode", "Heating House")
        else:
            logger.warning(f"Unknown combination of register values: reg28={reg28_value}, reg29={reg29_value}, reg30={reg30_value}")
            publish_mqtt("nibe/operation_mode", f"Unknown mode: reg28={reg28_value}, reg29={reg29_value}, reg30={reg30_value}")
        return None  # Avoid falling through to unhandled case

    # Handle additional heating using nibe/additional_heating_allowed
    if reg == 32:
        logger.debug(f"Register 32 (additional heating allowed) value: {value}")
        publish_mqtt("nibe/additional_heating_allowed", str(value))
        return None

    # Handle heating status using register 31
    if reg == 31:
        logger.debug(f"Register 31 (heating status) value: {value}")
        if value == 1:
            publish_mqtt("nibe/heating_status", "auto")
        elif value == 3:
            publish_mqtt("nibe/heating_status", "heating")
        elif value == 5:
            publish_mqtt("nibe/heating_status", "domestic_water")
        elif value == 6:
            publish_mqtt("nibe/heating_status", "additional_heating")
        return None

    # Handle temperature and flow registers
    if reg in [1, 5, 6, 7, 12, 23, 11, 13, 14, 15, 16, 17, 18, 21]:
        logger.debug(f"Register {reg} (temperature/flow) value: {value}")
        return float(unpack('h', pack('H', value))[0] / 10)

    # Handle general integer registers
    if reg in [0, 33, 34, 35, 36, 38, 44, 45, 46, 48, 100, 101, 102, 103, 104, 105]:
        logger.debug(f"Register {reg} (general integer) value: {value}")
        return int(value)

    # Handle signed values for heating curve and degree minutes
    if reg in [4, 8]:
        logger.debug(f"Register {reg} (signed value) value: {value}")
        return int(unpack('h', pack('H', value))[0] / 10)

    # Handle compressor starts
    if reg == 25:
        logger.debug(f"Register 25 (compressor starts) value: {value}")
        return int(value / 10)

    # Handle frequency, pressure, phase, and runtime registers
    if reg in [9, 10, 19, 20, 22, 24]:
        logger.debug(f"Register {reg} (frequency/pressure) value: {value}")
        return float(value / 10)

    # Handle hysteresis and BW registers
    if reg in [40, 47]:
        logger.debug(f"Register {reg} (hysteresis/BW reg) value: {value}")
        return float(value / 2)

    # Handle stop temperature and domestic water temperatures
    if reg in [43, 49, 50]:
        logger.debug(f"Register {reg} (temperature) value: {value}")
        return float(value)

    # Log unknown registers
    logger.warning(f"Register {reg} is not handled")
    return None




def run():
    logger.info("Starting the main loop...")

    # Publish availability as "online" at the start of the script
    publish_availability("online")

    # Publish discovery payloads for all sensors
    publish_discovery_payloads()

    mqtt_client.loop_start()
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
                        value = _decode(reg, raw)
                        if value is not None:
                            mqtt_topic = nibe_registers[reg]
                            publish_mqtt(mqtt_topic, value)
            except Exception as e:
                logger.warning(f"Error in Nibe data processing: {e}")
                time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Script interrupted, shutting down...")
    finally:
        # Publish availability as "offline" when the script is stopped
        publish_availability("offline")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    logger.info("Starting Nibe heat pump MQTT bridge")
    run()