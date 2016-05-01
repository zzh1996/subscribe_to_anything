from threading import Timer, Lock

class Repeater():
    def __init__(self, interval, function, *args, **kwargs):
        self._lock = Lock()
        self._timer = None
        self.function = function
        self.interval = interval
        self.args = args
        self.kwargs = kwargs
        self._stopped = True

    def start(self, from_run=False):
        if from_run or self._stopped:
            self._lock.acquire()
            self._stopped = False
            self._timer = Timer(self.interval, self._run)
            self._timer.setDaemon(True)
            self._timer.start()
            self._lock.release()

    def _run(self):
        self.start(from_run=True)
        self.function(*self.args, **self.kwargs)

    def stop(self):
        self._lock.acquire()
        self._stopped = True
        self._timer.cancel()
        self._lock.release()
