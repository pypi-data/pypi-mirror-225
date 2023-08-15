from uuid import UUID

from garlic import BaseEvent


class Subscriber:
    _consumed_events: dict[UUID, BaseEvent]

    def __init__(self):
        self._consumed_events = {}

    def __call__(self, event: BaseEvent):
        self.__check_duplicated_event(event)
        self._consumed_events[event.id] = event

    def __check_duplicated_event(self, event):
        if event.id in self._consumed_events:
            raise ValueError(f"Event {event.id} already consumed")
