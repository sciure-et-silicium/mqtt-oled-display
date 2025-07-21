import threading
import time
import logging
from database import DisplayItem

class DisplayManager(threading.Thread):
    def __init__(self, mqtt_client):
        threading.Thread.__init__(self)
        
        self._stop_event = threading.Event()

        self.mqtt_client = mqtt_client
        self.mqtt_client.set_message_callback(self.on_message)
        self.mqtt_client.set_connection_callback(self.on_connection)

        self.lock = threading.Lock()
        self.payloads: Dict[str, str] = {}
        self._display_refresh_requested = False
        self._display_items = []
        self._subscribed_topics = []
        self._subscription_refresh_requested = False
        logging.debug("DisplayManager initialized")

    def run(self):
        logging.info("DisplayManager thread started")
        try:
            while not self._stop_event.is_set():
                if self.display_refresh_requested() :
                    self.update_display()
                    self.display_refresh_done()
                time.sleep(0.1)
        except Exception as e:
            logging.error(f"Exception in DisplayManager thread: {e}", exc_info=True)
        finally:
            logging.debug("DisplayManager thread stopped")

    def stop(self):
        """Stop the thread and wait for termination"""
        logging.debug("Stopping DisplayManager requested")
        self._stop_event.set()
        self.join()
        logging.debug("DisplayManager fully stopped")

    def on_message(self, topic, payload):
        logging.debug(f"DisplayManager on_message {topic}: {payload}")
        with self.lock:
            self.payloads[topic] = payload
            self._display_refresh_requested = True
    
    def display_refresh_requested(self):
        with self.lock:
            return self._display_refresh_requested

    def display_refresh_done(self):
        with self.lock:
            self._display_refresh_requested = False

    def on_connection(self):
        logging.debug("DisplayManager on_connection")
#        self.mqtt_client.subscribe("z2m/sensor_temp_01_office")
        self.refresh_subscriptions()

    def update_display(self):
        logging.debug("DisplayManager update_display")

    def refresh_subscriptions(self):
        self.unsubscribe_all_topics()
        self.load_display_items()
        self.subscribe_all_topics()

    def unsubscribe_all_topics(self):
        logging.debug("DisplayManager unsubscribe_all_topics")
        for topic in self._subscribed_topics:
            self.mqtt_client.unsubscribe(topic)

    def load_display_items(self):
        logging.debug("DisplayManager load_display_items")
        self._display_items = DisplayItem.get_all_active()
        for item in self._display_items:
            print(f"ID: {item.id}, Nom: {item.name}, Topic: {item.mqtt_topic}")

    def subscribe_all_topics(self):
        logging.debug("DisplayManager subscribe_all_topics")
        for item in self._display_items:
            topic = item.mqtt_topic
            if topic in self._subscribed_topics:
                # already subscribed
                continue
            
            self._subscribed_topics.append(topic)
            self.mqtt_client.subscribe(topic)