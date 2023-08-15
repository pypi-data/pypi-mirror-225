from garlic import BaseEvent


class EventDispatcher:
    def __init__(self, event_handler: callable):
        self._event_handler = event_handler
        self._events: list = []

    def record(self, event: BaseEvent):
        self._events.append(event)

    def dispatch(self, event):
        for event in self._events:
            self._event_handler(event)

    def __call__(self, event):
        self._event_handler(event)

