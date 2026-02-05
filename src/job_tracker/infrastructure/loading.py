import sys
import threading
import time

class LoadingStatus:
    def __init__(self, text):
        self.text = text
        self._stop = threading.Event()

    def _run(self):
        dots = ""
        while not self._stop.is_set():
            dots = "." if dots == "..." else dots + "."
            sys.stdout.write(f'\r{self.text}{dots}')
            sys.stdout.flush()
            time.sleep(0.5)
        sys.stdout.write('\r')

    def start(self):
        self._stop.clear()
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def stop(self):
        self._stop.set()
        self._thread.join()
        print(f"✓ {self.text} Done")