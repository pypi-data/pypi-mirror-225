from typing import Callable

from garlic import EventHandler, EventDispatcher, BaseEvent
from garlic.types import DecoratedCallable


class Garlic:
    def __init__(self, config: dict = None):
        self.config = config or {}

        self._event_handler = EventHandler()
        self._event_dispatcher = EventDispatcher(event_handler=self._event_handler)

    def subscribe(self) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            self._event_handler.subscribe(
                subscriber=func,
            )
            return func

        return decorator

    def publish(self, event: BaseEvent):
        self._event_dispatcher(event=event)
