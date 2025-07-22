import logging

class Display:
    def __init__(self):
        logging.debug("Display init")

        self._cache = ""

    def render(self, str):
        if str == self._cache: return

        self._cache = str
        logging.debug(f"Display rendering \"{str}\"")
