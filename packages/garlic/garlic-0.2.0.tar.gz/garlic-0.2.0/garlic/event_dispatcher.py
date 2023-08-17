from garlic import BaseEvent


class EventDispatcher:
    def __init__(self, event_handler: callable):
        self._event_handler = event_handler

    def __call__(self, event):
        self._event_handler(event)

