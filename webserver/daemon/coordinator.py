import threading
import time
import logging
from database import DisplayItem

class Coordinator(threading.Thread):
    def __init__(self, mqtt_client):
        threading.Thread.__init__(self)
        
        self._stop_request = threading.Event()
        self.display_refresh_request = threading.Event()
        self.subscription_refresh_request = threading.Event()

        self.mqtt_client = mqtt_client
        self.mqtt_client.set_message_callback(self.on_message)
        self.mqtt_client.set_connection_callback(self.on_connection)

        self.lock = threading.Lock()
        self.payloads: Dict[str, str] = {}
        
        self._display_items = []
        self._current_displayed_item = 0
        self._subscribed_topics = []
        
        logging.debug("Coordinator initialized")

    def run(self):
        logging.info("Coordinator thread started")
        try:
            while not self._stop_request.is_set():
                
                # handle mqtt subscription refresh
                if self.subscription_refresh_request.is_set():
                    self.subscription_refresh()
                    self.subscription_refresh_request.clear()

                # handle display refresh
                if self.display_refresh_request.is_set() :
                    self.display_refresh()
                    self.display_refresh_request.clear()

                time.sleep(0.1)
            self._stop_request.clear()
        except Exception as e:
            logging.error(f"Exception in Coordinator thread: {e}", exc_info=True)
        logging.debug("Coordinator thread stopped")

    def stop(self):
        #Stop the thread and wait for termination
        logging.debug("Stopping Coordinator requested")
        self._stop_request.set()
        self.join()
        logging.debug("Coordinator fully stopped")

    def on_message(self, topic, payload):
        logging.debug(f"Coordinator on_message {topic}: {payload}")
        self.payload(topic, payload)
        self.display_refresh_request.set()
    
    def payload(self, topic, value=None):
        with self.lock:
            if value is not None:
                self.payloads[topic] = value
            return self.payloads[topic]            
    

    def on_connection(self):
        logging.debug("Coordinator on_connection")
        self.subscription_refresh_request.set()

    def display_refresh(self):
        logging.debug("Coordinator display_refresh")
        self.update_display()

    def update_display(self):
        logging.debug("Coordinator update_display")

    def subscription_refresh(self):
        logging.debug("Coordinator subscription_refresh")
        self.unsubscribe_all_topics()
        self.reload_from_db()
        self.subscribe_all_topics()
        

    def unsubscribe_all_topics(self):
        logging.debug("Coordinator unsubscribe_all_topics")
        for topic in self._subscribed_topics:
            self.mqtt_client.unsubscribe(topic)

    def reload_from_db(self):
        logging.debug("Coordinator reload_from_db")
        self._current_displayed_item = 0
        self._display_items = DisplayItem.get_all_active()
        for item in self._display_items:
            logging.debug(f"ID: {item.id}, Nom: {item.name}, Topic: {item.mqtt_topic}")

    def subscribe_all_topics(self):
        logging.debug("Coordinator subscribe_all_topics")
        for item in self._display_items:
            topic = item.mqtt_topic
            if topic in self._subscribed_topics:
                # already subscribed
                continue
            
            self._subscribed_topics.append(topic)
            self.mqtt_client.subscribe(topic)