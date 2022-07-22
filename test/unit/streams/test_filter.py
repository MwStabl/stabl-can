from typing import Generator

import pytest

from communicator.streams.datasource import MessageType, GenericMessage, Datasource
from communicator.streams.filter import MsgFilters, MessageFilter


@pytest.fixture
def message_filter_all_active() -> Generator[MessageFilter, None, None]:
    message_filter = MessageFilter()
    message_filter._active_filters = [
        MsgFilters.suppress_hc,
        MsgFilters.suppress_heartbeat,
        MsgFilters.suppress_can,
        MsgFilters.suppress_modbus,
        MsgFilters.suppress_uoc,
        MsgFilters.suppress_logging
    ]
    yield message_filter


def test_activate_filters() -> None:
    message_filter = MessageFilter()
    for filtertype in [
        MsgFilters.suppress_hc,
        MsgFilters.suppress_heartbeat,
        MsgFilters.suppress_can,
        MsgFilters.suppress_modbus,
        MsgFilters.suppress_uoc,
        MsgFilters.suppress_logging
    ]:
        message_filter.activate_filter(filtertype)
        assert filtertype in message_filter._active_filters


def test_deactivate_filters(message_filter_all_active: MessageFilter) -> None:
    for filtertype in [
        MsgFilters.suppress_hc,
        MsgFilters.suppress_heartbeat,
        MsgFilters.suppress_can,
        MsgFilters.suppress_modbus,
        MsgFilters.suppress_uoc,
        MsgFilters.suppress_logging
    ]:
        message_filter_all_active.deactivate_filter(filtertype)
        assert filtertype not in message_filter_all_active._active_filters
    assert message_filter_all_active._active_filters == []


def test_deactivate_inactive_filter() -> None:
    message_filter = MessageFilter()
    for filtertype in [
        MsgFilters.suppress_hc,
    ]:
        message_filter.deactivate_filter(filtertype)


def test_filtering() -> None:
    msg_hc = GenericMessage(content="", datasource=Datasource.Canbus, classification=MessageType.healthcare)
    msg_hb = GenericMessage(content="", datasource=Datasource.Canbus, classification=MessageType.heartbeat)
    message_filter = MessageFilter()
    message_filter.activate_filter(MsgFilters.suppress_hc)
    assert message_filter.suppress(msg_hc)
    assert not message_filter.suppress(msg_hb)
