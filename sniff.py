from common.getter import StablCanBus
from common.modbus import Modbus
from decode.visualise import visualise

if __name__ == "__main__":
    can = StablCanBus()
    try:
        while True:
            new_msg = can.get_received_message()
            print(visualise(new_msg))
    except KeyboardInterrupt:
        print("End")
