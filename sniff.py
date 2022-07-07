from time import sleep

from common.can import StablCanBus
from common.modbus import Modbus
from decode.visualise import visualise

if __name__ == "__main__":
    can = StablCanBus()
    modbus = Modbus()
    for bus in [can, modbus]:
        bus.start()
    try:
        while True:
            if can.new_msg:
                print(visualise(can.get_new_message()))
            if modbus.new_msg:
                print(modbus.get_new_message())
            sleep(0.1)
    except KeyboardInterrupt:
        print("End")
    finally:
        for bus in [can, modbus]:
            bus.terminate()
