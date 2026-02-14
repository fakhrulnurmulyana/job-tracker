import sys
import threading
import time

class LoadingStatus:
    """
    Display a console-based animated loading indicator.

    This class runs a background thread that prints a dynamic
    loading message with animated dots until explicitly stopped.
    """
    def __init__(self, text):
        """
        Initialize the loading indicator.

        Args:
            text (str): Base message displayed during loading.
        """
        self.text = text
        self._stop = threading.Event()

    def _run(self):
        """
        Execute the loading animation loop.

        This method runs in a separate thread and continuously
        updates the console output until the stop event is set.
        """
        dots = ""
        while not self._stop.is_set():
            dots = "." if dots == "..." else dots + "."
            sys.stdout.write(f'\r{self.text}{dots}')
            sys.stdout.flush()
            time.sleep(0.5)
        sys.stdout.write('\r')

    def start(self):
        """
        Start the loading animation in a background thread.
        """
        self._stop.clear()
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def _stop_event(self):
        """
        Signal the loading thread to stop.
        """
        self._stop.set()

    def true_stop(self):
        """
        Stop the loading animation and display a success message.

        This method waits for the background thread to finish
        and prints a completion indicator.
        """
        self._stop_event()
        self._thread.join()
        print(f"✓ {self.text} Done")

    def false_stop(self):
        """
        Stop the loading animation without printing a success message.
        """
        self._stop_event()