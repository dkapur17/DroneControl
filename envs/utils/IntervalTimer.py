from threading import Thread, Event
from time import sleep

class StoppableThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.stop_event = Event()

    def stop(self):
        self.stop_event.set()
        self.join()
            
class IntervalTimer(StoppableThread):

    def __init__(self, interval, func):
        super().__init__()
        self._interval = interval
        self._func = func

    def run(self):
        while not self.stop_event.is_set():
            self._func()
            sleep(self._interval/1000)