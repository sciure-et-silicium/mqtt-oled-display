
from database import init_database
from database import Configuration
from daemon.mqtt_client import MQTTClient
from daemon.display_manager import DisplayManager
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

display_manager = DisplayManager(mqtt_client)

try:
    mqtt_client.start()
    display_manager.start()

    # Keep the program running to receive messages
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping by user request")
finally:
    mqtt_client.stop()
    display_manager.stop()