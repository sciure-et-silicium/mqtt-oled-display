
from database import init_database
from daemon import Coordinator, Display, TermDisplay, MQTTClient
import time
import logging
import signal
from threading import Lock
from dotenv import load_dotenv
import helpers.pid as pid
import os

load_dotenv()

log_level = getattr(logging, os.environ.get('LOG_LEVEL', 'INFO').upper(), logging.INFO)
logging.basicConfig(level=log_level)

logging.info("Starting Daemon")

init_database()
 

# Create MQTT client instance
mqtt_client = MQTTClient(
    broker_host = os.environ.get("MQTT_HOST"),
    broker_port = int(os.environ.get("MQTT_PORT")),
    username = os.environ.get("MQTT_USERNAME"),
    password = os.environ.get("MQTT_PASSWORD"),
    client_id = os.environ.get("MQTT_CLIENT_ID"),
    qos=1
)


display = TermDisplay()
coordinator = Coordinator(display, mqtt_client)

pid.create_pid_file()
logging.debug(f"PID file created ({pid.read_pid_file()})")

try:
    mqtt_client.start()
    coordinator.start()

    # Keep the program running to receive messages
    while True:
        time.sleep(5)

except KeyboardInterrupt:
    logging.debug("Stopping by user request")

logging.info("Stopping Daemon")

mqtt_client.stop()
coordinator.stop()

pid.cleanup_pid_file()