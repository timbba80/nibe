import logging
import paho.mqtt.client as mqtt

# Setup logger
logger = logging.getLogger('NIBE_MQTT')

# Initialize MQTT client
mqtt_client = mqtt.Client()
mqtt_client.reconnect_delay_set(min_delay=1, max_delay=60)
mqtt_client.username_pw_set(username="usr", password="pswd")  # Set MQTT broker username and password
mqtt_client.connect("0.0.0.0", 1883, 60)  # Set MQTT broker IP address and port

def publish_mqtt(topic, message):
    """Publish a message to an MQTT topic."""
    try:
        mqtt_client.publish(topic, message)
        logger.info(f"Published {message} to {topic}")
    except Exception as e:
        logger.error(f"Failed to publish {message} to {topic}: {e}")

def publish_availability(status):
    """Publish the availability status of the device."""
    publish_mqtt("nibe/status", status)

def publish_discovery_payloads():
    """Publish Home Assistant discovery payloads."""
    from constants import mqtt_discovery_sensors  # Avoid circular import

    for sensor, config in mqtt_discovery_sensors.items():
        discovery_topic = f"homeassistant/sensor/{config['unique_id']}/config"

        payload = {
            "name": config["name"],
            "state_topic": config["state_topic"],
            "unique_id": config["unique_id"],
            "availability_topic": "nibe/status",
            "payload_available": "online",
            "payload_not_available": "offline",
            "device": {
                "identifiers": ["nibe_heat_pump"],
                "name": "Mitsubishi heavy industries Heat Pump",
                "manufacturer": "MHI",
                "model": "HMA100V",
                "sw_version": "1.0",
            },
        }

        # Add optional fields
        if "unit_of_measurement" in config:
            payload["unit_of_measurement"] = config["unit_of_measurement"]
        if "device_class" in config:
            payload["device_class"] = config["device_class"]
        if "value_template" in config:
            payload["value_template"] = config["value_template"]

        mqtt_client.publish(discovery_topic, str(payload).replace("'", '"'), qos=0, retain=True)
        logger.info(f"Published MQTT discovery payload for {config['name']}")

mqtt_client.loop_start()
