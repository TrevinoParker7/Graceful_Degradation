"""
Asynchronous Local Event Bus for GracefulOS
"""

import asyncio
import logging
from collections import defaultdict
from typing import Callable, Coroutine, Dict, List, Any
from .events import BaseEvent, EventType

logger = logging.getLogger("GracefulOS.EventBus")

SubscriberCallback = Callable[[BaseEvent], Coroutine[Any, Any, None]]

class EventBus:
    def __init__(self):
        self._subscribers: Dict[EventType, List[SubscriberCallback]] = defaultdict(list)
        self._global_subscribers: List[SubscriberCallback] = []
        self._history: List[BaseEvent] = []
        self._max_history: int = 1000
        self._lock = asyncio.Lock()

    def subscribe(self, event_type: EventType, callback: SubscriberCallback) -> None:
        """Subscribe a coroutine callback to a specific event type."""
        self._subscribers[event_type].append(callback)

    def subscribe_all(self, callback: SubscriberCallback) -> None:
        """Subscribe a coroutine callback to all events."""
        self._global_subscribers.append(callback)

    def unsubscribe(self, event_type: EventType, callback: SubscriberCallback) -> None:
        if callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(callback)

    async def publish(self, event: BaseEvent) -> None:
        """Publish an event to all relevant subscribers asynchronously."""
        async with self._lock:
            self._history.append(event)
            if len(self._history) > self._max_history:
                self._history.pop(0)

        callbacks = list(self._subscribers.get(event.event_type, [])) + list(self._global_subscribers)
        if not callbacks:
            return

        tasks = []
        for cb in callbacks:
            try:
                tasks.append(asyncio.create_task(cb(event)))
            except Exception as e:
                logger.error(f"Error creating task for callback {cb}: {e}")

        if tasks:
            # Let subscribers complete, catching and logging any errors
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for res in results:
                if isinstance(res, Exception):
                    logger.error(f"Subscriber execution error: {res}")

    def get_recent_events(self, limit: int = 50) -> List[BaseEvent]:
        """Get recent in-memory event stream."""
        return self._history[-limit:]

# Singleton instance
event_bus = EventBus()
