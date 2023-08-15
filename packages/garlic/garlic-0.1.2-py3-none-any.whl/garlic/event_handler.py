from typing import Type

from garlic.base_event import BaseEvent


class EventHandler:
    subscriptions: dict[str, list[callable]]

    def __init__(self):
        self.subscriptions: dict[Type[BaseEvent], callable] = {}

    def subscribe(self, event_class: Type[BaseEvent], subscriber: callable):
        self._validate_event_class(event_class)

        if event_class not in self.subscriptions:
            self.subscriptions[event_class] = []

        self.subscriptions[event_class].append(subscriber)

    def trigger(self, event: BaseEvent):
        event_class = event.__class__

        if event_class in self.subscriptions:
            for subcriber in self.subscriptions[event_class]:
                subcriber(event)

    def _validate_event_class(self, event_class: Type[BaseEvent]):
        if not issubclass(event_class, BaseEvent):
            raise ValueError("event_class should be a subclass of BaseEvent")

    def __call__(self, event: BaseEvent):
        self.trigger(event)

