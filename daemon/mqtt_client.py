# daemon/mqtt_client.py
import paho.mqtt.client as mqtt
import json
import logging
from typing import List, Optional, Dict
from threading import Lock
import os


class MQTTClient:
    """A basic MQTT client class that handles connection, subscription and message processing."""

    def __init__(self,
                 broker_host: str,
                 broker_port: int = 1883,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 client_id: Optional[str] = None,
                 qos: int = 0):
        """
        Initialize the MQTT client.

        Args:
            broker_host: MQTT broker hostname or IP address
            broker_port: MQTT broker port (default: 1883)
            username: Username for authentication (optional)
            password: Password for authentication (optional)
            client_id: Client ID (auto-generated if None)
            qos: Quality of Service level (0, 1, or 2)
        """
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.username = username
        self.password = password
        self.client_id = client_id or f"python-mqtt-{mqtt._generate_id()}"
        self.qos = qos
        

        self._message_callback = None
        self._connection_callback = None

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

    def start(self) -> None:
        """Connect to the MQTT broker and start the network loop."""
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_start()
        except Exception as e:
            logging.error(f"MQTT Connection error: {e}")
            raise

    def _on_connect(self, client, userdata, flags, rc) -> None:
        """Callback for when the client connects to the broker."""
        if rc != 0:
            logging.error(f"MQTT Connection failed with code: {rc}")
            return
        
        logging.info("Connected to MQTT broker")
        if self._connection_callback is None: return
        self._connection_callback()


    def stop(self) -> None:
        """Disconnect from the MQTT broker."""
        try:
            self.client.loop_stop()
            self.client.disconnect()
            logging.debug("MQTT client disconnected")
        except Exception as e:
            logging.error(f"MQTT Disconnection error: {e}")

    
    def _on_disconnect(self, client, userdata, rc) -> None:
        """Callback for when the client disconnects from the broker."""
        if rc != 0:
            logging.warning(f"MQTT Unexpected disconnection, code: {rc}")
        else:
            logging.debug("MQTT Normal disconnection")

    def subscribe(self, topic: str, qos: Optional[int] = None) -> None:
        """
        Subscribe to a new topic.

        Args:
            topic: Topic to subscribe to
            qos: Quality of Service level (uses default if None)
        """
        logging.debug(f"MQTT subscribe topic={topic}")
        qos = qos or self.qos
        try:
            self.client.subscribe(topic, qos=qos)
        except Exception as e:
            logging.error(f"MQTT Subscription error: {e}")

    def unsubscribe(self, topic: str) -> bool:
        logging.debug(f"MQTT unsubscribe topic={topic}")
        try:
            result, _ = self.client.unsubscribe(topic)
            if result == mqtt.MQTT_ERR_SUCCESS:
                return True

            logging.error(f"MQTT unsubscription error: {result}")
        except Exception as e:
            logging.error(f"MQTT unsubscription error: {e}")
        return False

    def _on_message(self, client, userdata, msg) -> None:
        """Callback for when a message is received from the broker."""
        if self._message_callback is None: return

        try:
            payload = msg.payload.decode('utf-8')
            logging.debug(f"MQTT Message received on {msg.topic}: {payload}")
            self._message_callback(msg.topic, payload)
        
        except Exception as e:
            logging.error(f"MQTT Error processing message: {e}", exc_info=True)
            os._exit(1)

    def set_message_callback(self, callback) :
        self._message_callback = callback
   
    def set_connection_callback(self, callback) :
        self._connection_callback = callback