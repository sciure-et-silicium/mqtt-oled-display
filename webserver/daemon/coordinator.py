import threading
import time
import logging
import os
from database import DisplayItem
from helpers.render import render_template

class Coordinator(threading.Thread):
    def __init__(self, display, mqtt_client):
        threading.Thread.__init__(self)
        
        self._stop_request = threading.Event()
        self.subscription_refresh_request = threading.Event()

        self.mqtt_client = mqtt_client
        self.mqtt_client.set_message_callback(self.on_message)
        self.mqtt_client.set_connection_callback(self.on_connection)

        self.lock = threading.Lock()
        self.payloads: Dict[str, str] = {}
        
        self._display_items = []
        self._current_displayed_item = 0
        self._subscribed_topics = []
        self._timer = time.time()

        self._display = display
        
        logging.debug("Coordinator initialized")

    def run(self):
        logging.info("Coordinator thread started")
        try:
            while not self._stop_request.is_set():
                
                # handle mqtt subscription refresh
                if self.subscription_refresh_request.is_set():
                    self.subscription_refresh()
                    self.subscription_refresh_request.clear()

                # time.sleep(0.05) # max 20 FPS
                time.sleep(1)

                self.display()
                
            self._stop_request.clear()
        except Exception as e:
            logging.error(f"Exception in Coordinator thread: {e}", exc_info=True)
            os._exit(1)
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
    
    def payload(self, topic, value=None):
        with self.lock:
            if value is not None:
                self.payloads[topic] = value
            return self.payloads.get(topic)
    

    def on_connection(self):
        logging.debug("Coordinator on_connection")
        self.subscription_refresh_request.set()

    def display(self):
        now = time.time()
        delta = now - self._timer
        
        if len(self._display_items) == 0: # just in case
            self._display.render("No active display item")
            return

        item = self._display_items[self._current_displayed_item];
        
        if delta > item.duration:
            self._timer = now
            # duration for display item is over, so go for the next one
            self._current_displayed_item = (self._current_displayed_item + 1) % len(self._display_items)
            item = self._display_items[self._current_displayed_item];

            logging.debug(f"switching to next display item. ID: {item.id}, Nom: {item.name}, Topic: {item.mqtt_topic}")

        # update display in all cases
        logging.debug(f"updating display with display item. ID: {item.id}, Nom: {item.name}, Topic: {item.mqtt_topic}")
        try:

            render_result = render_template(
                item.render_template,
                self.payload(item.mqtt_topic)
            )

            self._display.render(
                render_result
            )
        except Exception as e:
            logging.Error(f"Render error: {str(e)}")
            display.render(f"Render error: {str(e)}")
        


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