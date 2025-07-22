import logging

class Display:
    def __init__(self):
        logging.debug("Display init")

    def render(self, string):
        logging.debug(f"Display rendering \"{string}\"")