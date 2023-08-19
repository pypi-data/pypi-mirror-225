from typing import Callable, Union, Any, Dict, Set


class EventEmitter():
    def __init__(self) -> None:
        self.subscriptions: Dict[str, Set[Callable]] = {}

    def subscribe(self, topic: str, callback: Callable):
        self._validate_topic(topic)
        self._validate_callback(callback)
        handlers = self.subscriptions.get(topic, set())
        handlers.add(callback)
        self.subscriptions[topic] = handlers
        return Subscription(topic, callback, handlers)

    def emit(self, topic: str, data: Union[Any, None]):
        self._validate_topic(topic)
        if not (topic in self.subscriptions):
            raise EventEmitterException("There is not such a topic")
        for callable in self.subscriptions.get(topic).copy():
            try:
                callable(topic, data)
            except:
                pass

    def _validate_topic(self, topic: str):
        if not topic:
            raise EventEmitterException("Topic is required")

    def _validate_callback(self, callback: Callable):
        if not callback:
            raise EventEmitterException("Callable is required")


class EventEmitterException(Exception):
    def __init__(self, message: str = "EventEmitter error"):
        super().__init__(message)

    def __str__(self):
        original_message = super().__str__()
        return f"EventEmitter error: {original_message}"


class Subscription():
    def __init__(self, topic: str, callback: Callable, handlers: Set[Callable]):
        self.handlers: Set = handlers
        self.callback: Callable = callback
        self.topic: str = topic

    def unsubscribe(self):
        if self.callback in self.handlers:
            self.handlers.remove(self.callback)
        else:
            raise EventEmitterException(
                f"There is not callback subscribed to topic={self.topic}")
