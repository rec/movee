from dataclasses import dataclass
from typing import Callable
import threading
import time


@dataclass
class Waiter:
    callback: Callable = None
    duration: float = 1
    cycle_time: float = 0.1

    def is_alive(self):
        return (t := getattr(self, 'thread', None)) and t.is_alive()

    def start(self):
        if self.callback:
            self._finish = time.time() + self.duration
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.running = True
            self.thread.start()

    def stop(self):
        self.running = False

    def run(self):
        while self.running and (remains := self._finish - time.time()) > 0:
            time.sleep(min(remains, self.cycle_time))

        if self.running:
            self.callback()
