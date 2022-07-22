from __future__ import annotations

from enum import Enum
from typing import List, Callable

from communicator.streams.datasource import GenericMessage, MessageType, Datasource


class MessageFilter:
    """
    Implements message filtering.

    Methods:
    --------
    activate_filter(msg_filter: MsgFilters)
        activates a filter from the MsgFilters-Enum

    deactivate_filter(msg_filter: MsgFilters)
        deactivates a filter from the MsgFilters-Enum

    suppress(message):
        returns true if a message shall be suppressed according to the filter rules
    """
    def __init__(self):
        self._active_filters: List[Callable] = []

    def activate_filter(self, msg_filter: MsgFilters):
        self._active_filters.append(msg_filter)

    def deactivate_filter(self, msg_filter: MsgFilters):
        try:
            self._active_filters.remove(msg_filter)
        except ValueError:
            pass

    def suppress(self, message: GenericMessage) -> bool:
        """ returns true if any of the filters returns true """
        return any([active_filter(message) for active_filter in self._active_filters])

    @staticmethod
    def suppress_hc(message: GenericMessage) -> bool:
        """ returns true, if message is a hc message (and should therefore be suppressed)"""
        return message.classification == MessageType.healthcare

    @staticmethod
    def suppress_heartbeat(message: GenericMessage) -> bool:
        return message.classification == MessageType.heartbeat

    @staticmethod
    def suppress_can(message: GenericMessage) -> bool:
        return message.datasource == Datasource.Canbus

    @staticmethod
    def suppress_modbus(message: GenericMessage) -> bool:
        return message.datasource == Datasource.Modbus

    @staticmethod
    def suppress_uoc(message: GenericMessage) -> bool:
        return message.datasource == Datasource.UoC

    @staticmethod
    def suppress_logging(message: GenericMessage) -> bool:
        return message.classification == MessageType.logging


class MsgFilters(Enum):
    suppress_hc = MessageFilter.suppress_hc
    suppress_heartbeat = MessageFilter.suppress_heartbeat
    suppress_can = MessageFilter.suppress_can
    suppress_modbus = MessageFilter.suppress_modbus
    suppress_uoc = MessageFilter.suppress_uoc
    suppress_logging = MessageFilter.suppress_logging
