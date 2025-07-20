
from database import init_database
from database import Configuration
from daemon.mqtt_client import MQTTClient
import time
import logging

init_database()

 # Configure logging
logging.basicConfig(level=logging.DEBUG)


# Create MQTT client instance
mqtt_client = MQTTClient(
    broker_host = Configuration.get_value_by_key("mqtt.broker"),
    broker_port = int(Configuration.get_value_by_key("mqtt.port")),
    username = Configuration.get_value_by_key("mqtt.username"),
    password = Configuration.get_value_by_key("mqtt.password"),
    client_id = Configuration.get_value_by_key("mqtt.client_id"),
    qos=1
)

try:
    # Connect to broker
    mqtt_client.start()

    # Example publish
    mqtt_client.subscribe("z2m/sensor_temp_01_office")

    # Keep the program running to receive messages
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping by user request")
finally:
    mqtt_client.stop()