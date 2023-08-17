from typing import Type, Callable

from .base_event import BaseEvent
from .utils import get_typed_signature


class EventHandler:
    subscriptions: dict[str, list[Callable]]

    def __init__(self):
        self.subscriptions: dict[Type[BaseEvent], Callable] = {}

    def subscribe(self, subscriber: Callable):
        signature = get_typed_signature(subscriber)
        signature_params = signature.parameters

        assert "event" in signature_params, "Subscriber should have an event parameter"

        event_class = signature_params["event"].annotation

        if event_class not in self.subscriptions:
            self.subscriptions[event_class] = []

        self.subscriptions[event_class].append(subscriber)

    def trigger(self, event: BaseEvent):
        event_class = event.__class__

        if event_class in self.subscriptions:
            for subscriber in self.subscriptions[event_class]:
                subscriber(event)

    def __call__(self, event: BaseEvent):
        self.trigger(event)

