import logging
import paho.mqtt.client as mqtt

logger = logging.getLogger('NIBE')

mqtt_client = mqtt.Client()
mqtt_client.reconnect_delay_set(min_delay=1, max_delay=60)
mqtt_client.username_pw_set(username="usrname", password="pswd")
mqtt_client.connect("0.0.0.0", 1883, 60)

def publish_mqtt(topic, message):
    mqtt_client.publish(topic, message)
    logger.info(f"Published {message} to {topic}")

def publish_availability(status):
    mqtt_client.publish("nibe/status", status)
    logger.info(f"Published availability status: {status}")

def publish_discovery_payloads(discovery_sensors):
    for sensor, config in discovery_sensors.items():
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
                "model": "HMA100v",
                "sw_version": "1.0"
            }
        }
        if config.get("unit_of_measurement"):
            payload["unit_of_measurement"] = config["unit_of_measurement"]
        if config.get("device_class"):
            payload["device_class"] = config["device_class"]
        if config.get("value_template"):
            payload["value_template"] = config["value_template"]
        mqtt_client.publish(discovery_topic, str(payload).replace("'", '"'), qos=0, retain=True)
        logger.info(f"Published MQTT discovery payload for {config['name']}")
