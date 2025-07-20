# daemon/mqtt_client.py
import paho.mqtt.client as mqtt
import json
import logging
from typing import List, Optional, Union

class MQTTClient:
    """A basic MQTT client class that handles connection, subscription and message processing."""

    def __init__(self,
                 broker_host: str,
                 broker_port: int = 1883,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 client_id: Optional[str] = None,
                 topics: Optional[List[str]] = None,
                 qos: int = 0):
        """
        Initialize the MQTT client.

        Args:
            broker_host: MQTT broker hostname or IP address
            broker_port: MQTT broker port (default: 1883)
            username: Username for authentication (optional)
            password: Password for authentication (optional)
            client_id: Client ID (auto-generated if None)
            topics: List of topics to subscribe to (optional)
            qos: Quality of Service level (0, 1, or 2)
        """
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.username = username
        self.password = password
        self.client_id = client_id or f"python-mqtt-{mqtt._generate_id()}"
        self.topics = topics or []
        self.qos = qos

        # Initialize MQTT client
        self.client = mqtt.Client(client_id=self.client_id)
        self._configure_client()

    def _configure_client(self) -> None:
        """Configure the MQTT client with callbacks and settings."""
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)

    def _on_connect(self, client, userdata, flags, rc) -> None:
        """Callback for when the client connects to the broker."""
        if rc == 0:
            logging.info("Connected to MQTT broker")
            for topic in self.topics:
                client.subscribe(topic, qos=self.qos)
                logging.info(f"Subscribed to topic: {topic}")
        else:
            logging.error(f"Connection failed with code: {rc}")

    def _on_message(self, client, userdata, msg) -> None:
        """Callback for when a message is received from the broker."""
        try:
            payload = msg.payload.decode('utf-8')
            logging.info(f"Message received on {msg.topic}: {payload}")

            # Try to parse JSON if possible
            try:
                data = json.loads(payload)
                logging.info(f"JSON payload: {json.dumps(data, indent=2)}")
            except json.JSONDecodeError:
                pass

        except Exception as e:
            logging.error(f"Error processing message: {e}")

    def _on_disconnect(self, client, userdata, rc) -> None:
        """Callback for when the client disconnects from the broker."""
        if rc != 0:
            logging.warning(f"Unexpected disconnection, code: {rc}")
        else:
            logging.info("Normal disconnection")

    def start(self) -> None:
        """Connect to the MQTT broker and start the network loop."""
        print("def start(self) -> None:")
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_start()
        except Exception as e:
            logging.error(f"Connection error: {e}")
            raise

    def stop(self) -> None:
        """Disconnect from the MQTT broker."""
        try:
            self.client.loop_stop()
            self.client.disconnect()
            logging.info("MQTT client disconnected")
        except Exception as e:
            logging.error(f"Disconnection error: {e}")

    def subscribe(self, topic: str, qos: Optional[int] = None) -> None:
        """
        Subscribe to a new topic.

        Args:
            topic: Topic to subscribe to
            qos: Quality of Service level (uses default if None)
        """
        qos = qos or self.qos
        try:
            self.client.subscribe(topic, qos=qos)
            if topic not in self.topics:
                self.topics.append(topic)
            #logging.info(f"Subscribed to topic: {topic}")
        except Exception as e:
            logging.error(f"Subscription error: {e}")
