from threading import Timer

import npyscreen

from common.can import StablCanBus
from decode.visualise import visualise


class FifoBuffer(list):
    def __init__(self, max_size: int, *args, **kwargs):
        self._m = max_size
        super().__init__(*args, **kwargs)

    def put(self, val):
        if len(self) >= self._m:
            self.pop(0)
        self.append(val)


msg_buffer = FifoBuffer(max_size=1024)


class myEmployeeForm(npyscreen.ActionForm):
    def afterEditing(self):
        self.parentApp.setNextForm(None)
        self.add_handlers({"n": self.change_stuff})

    def create(self):
        self._can = StablCanBus()
        self._can.start()
        self._display_hc: bool = True
        self.myStatus = self.add(npyscreen.Textfield, name="status", value="all shown")
        self.myMulti = self.add(npyscreen.MultiLine, name="dingsi", values=msg_buffer, hidden=False)
        self.myMulti.add_handlers({"^N": self.change_stuff})

    def change_stuff(self, *args, **kwargs):
        if self._display_hc:
            self.myMulti.values = [msg for msg in msg_buffer if "HC Stuff" not in msg]
            self._display_hc = False
        else:
            self.myMulti.values = msg_buffer
            self._display_hc = True
        self.myMulti.display()

    def update_buffer(self):
        msg_buffer.put(visualise(self._can.get_new_message()))

    def on_cancel(self):
        print("u suck")


class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", myEmployeeForm, name="New Employee")

        # A real application might define more forms here.......


if __name__ == "__main__":
    TestApp = MyApplication().run()
