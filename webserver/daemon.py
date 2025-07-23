
from database import init_database
from database import Configuration
from daemon import Coordinator, TermDisplay, MQTTClient
import time
import logging
import signal
from threading import Lock


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

display = TermDisplay()

coordinator = Coordinator(display, mqtt_client)

# handle sigusr1 with thread safety
sig_usr1_received = False
var_lock = Lock()
def handle_sigusr1(signum, frame):
    logging.info("Received USR1 signal")
    with var_lock:
        sig_usr1_received = True

signal.signal(signal.SIGUSR1, handle_sigusr1)


try:
    mqtt_client.start()
    coordinator.start()

    # Keep the program running to receive messages
    while True:
        with var_lock:
            if sig_usr1_received:
                sig_usr1_received = False
                coordinator.reload()
        
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping by user request")
finally:
    mqtt_client.stop()
    coordinator.stop()


        