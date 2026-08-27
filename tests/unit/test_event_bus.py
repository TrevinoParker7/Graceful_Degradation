"""
Unit Tests for Async Local Event Bus
"""

import pytest
import asyncio
from core.events.bus import EventBus
from core.events.events import BaseEvent, EventType

@pytest.mark.asyncio
async def test_event_bus_pubsub():
    bus = EventBus()
    received = []

    async def sample_handler(event: BaseEvent):
        received.append(event)

    bus.subscribe(EventType.AGENT_REGISTERED, sample_handler)

    test_event = BaseEvent(
        event_type=EventType.AGENT_REGISTERED,
        agent_id="test-agent",
        data={"mission": "unit_test"},
    )

    await bus.publish(test_event)
    assert len(received) == 1
    assert received[0].agent_id == "test-agent"
