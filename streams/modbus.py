#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Testscript for modbus logging interface. Needs pyModbusTCP
# and minimalmodbus installed:
#
# pip install [--user] pyModbusTCP
# pip install [--user] minimalmodbus
#
# Reads and prints the boards log buffer in a regular interval.
import os
import sys
import time
from queue import Queue
from threading import Lock, Thread

import minimalmodbus
from pyModbusTCP.client import ModbusClient

from streams.datasource import StablDatasource
from streams.settings import *


class StablModbus(StablDatasource):
    interval = 0.1
    prompt = ""
    error_counter = 0

    def __init__(self, prompt=""):
        super().__init__()
        self._modbus_lock = Lock()
        self._modbus = self._setupModbus()
        reconnect_modbus(self._modbus)
        self.prompt = prompt

    @staticmethod
    def _setupModbus() -> ModbusClient:
        modbus = ModbusClient(timeout=MODBUS_TIMEOUT_TIME)
        modbus.host = SERVER_HOST
        modbus.port = SERVER_PORT
        return modbus

    def send_command(self, command: str) -> None:
        if len(command) >= MODBUS_HOLDING_CMD_LEN * 2:
            print("Command to long")
        else:
            print("Sending Modbus command: {}".format(command))

            # encode string into 16 bit register list using minimalmodbus helper functions
            bytestring = minimalmodbus._textstring_to_bytestring(command, MODBUS_HOLDING_CMD_LEN)
            valuelist = minimalmodbus._bytestring_to_valuelist(bytestring, MODBUS_HOLDING_CMD_LEN)

            # send register list via modbus
            self._modbus_lock.acquire()
            self._modbus.write_multiple_registers(MODBUS_HOLDING_CMD_ADDR - 1, valuelist)
            self._modbus_lock.release()

    def setInterval(self, interval):
        self.interval = interval

    def getAndPrintLogBuffer(self, idx):
        bufferaddr = int(MODBUS_INPUT_LOGBUF_ADDR + ((idx * LOG_BUFFER_SIZE) / 2))

        reglist = self._modbus.read_input_registers(bufferaddr - 1, int(LOG_BUFFER_SIZE / 2))

        # decode register list to string using minimalmodbus helper functions
        bytestring = minimalmodbus._valuelist_to_bytestring(reglist, int(LOG_BUFFER_SIZE / 2))
        print(minimalmodbus._bytestring_to_textstring(bytestring, int(LOG_BUFFER_SIZE / 2)))

    def _addToBuffer(self, idx):
        bufferaddr = int(MODBUS_INPUT_LOGBUF_ADDR + ((idx * LOG_BUFFER_SIZE) / 2))

        reglist = self._modbus.read_input_registers(bufferaddr - 1, int(LOG_BUFFER_SIZE / 2))

        # decode register list to string using minimalmodbus helper functions
        bytestring = minimalmodbus._valuelist_to_bytestring(reglist, int(LOG_BUFFER_SIZE / 2))
        message = minimalmodbus._bytestring_to_textstring(bytestring, int(LOG_BUFFER_SIZE / 2))
        self._buffer.put(message)

    def run(self):
        self.running = True
        while self.running:
            time.sleep(self.interval)
            self._modbus_lock.acquire()

            # get logbuffer status bits, which indicate which logbuffer holds a new entry
            logbits = self._modbus.read_discrete_inputs(MODBUS_INPUT_LOGSTATUS_ADDR - 1, MODBUS_INPUT_LOGSTATUS_LEN)

            if logbits is None:
                print("Logthread: modbus read error, system might be disconnected, attempting reconnect....")
                reconnect_modbus(self._modbus)
                self._modbus_lock.release()
                self.error_counter += 1
                if self.error_counter > MODBUS_TIMEOUT_COUNTER:
                    print("Had an error 5 times in succession, will exit now")
                    os._exit(0)
                continue

            self.error_counter = 0

            # get last zero in the list, from there we start iterating over the log buffers
            # this way we start with the oldest entry and proceed to the newest one
            try:
                start = len(logbits) - logbits[::-1].index(0) - 1
            except ValueError:
                start = 0

            idxlist = list(range(start, len(logbits))) + list(range(0, start))

            no_output = True
            for idx in idxlist:
                if logbits[idx] == 1:
                    if no_output:
                        print()
                        no_output = False
                    self._addToBuffer(idx)
                    # self.getAndPrintLogBuffer(idx)

            if no_output == False:
                print(self.prompt, end="")
                sys.stdout.flush()

            self._modbus_lock.release()

    def terminate(self):
        self.running = False
        self.join()


# only call from within lockbus lock
def reconnect_modbus(modbus_client):
    modbus_client.close()
    if not modbus_client.is_open:
        reconnect_counter = 0
        while not modbus_client.open() and reconnect_counter < 5:
            print("unable to connect to " + SERVER_HOST + ":" + str(SERVER_PORT))
            reconnect_counter = reconnect_counter + 1
        if reconnect_counter >= MODBUS_TIMEOUT_COUNTER:
            print("Couldnt reconnect, exiting.")
            os._exit(0)
        print("Reconnected!")
    else:
        print("Just closed it an still open, will kill process, please check for other processes running")
        os._exit(0)
