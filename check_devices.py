from threading import Thread, Lock
from time import perf_counter
from sys import stderr
import socket

BASE_IP = "192.168.0.%i"
PORT = 2333


class Threader:
    """
    This is a class that calls a list of functions in a limited number of
    threads. It uses locks to make sure the data is thread safe.
    Usage:
        from time import sleep

        def function(i):
            sleep(2)
            with threader.print_lock:
                print(i)

        threader = Threader(10) # The maximum number of threads = 10
        for i in range(20):
            threader.append(function, i)
        threader.start()
        threader.join()

    This class also provides a lock called: `<Threader>.print_lock`
    """

    def __init__(self, threads=30):
        self.thread_lock = Lock()
        self.functions_lock = Lock()
        self.functions = []
        self.threads = []
        self.nthreads = threads
        self.running = True
        self.print_lock = Lock()

    def stop(self) -> None:
        # Signal all worker threads to stop
        self.running = False

    def append(self, function, *args) -> None:
        # Add the function to a list of functions to be run
        self.functions.append((function, args))

    def start(self) -> None:
        # Create a limited number of threads
        for i in range(self.nthreads):
            thread = Thread(target=self.worker, daemon=True)
            # We need to pass in `thread` as a parameter so we
            # have to use `<threading.Thread>._args` like this:
            thread._args = (thread,)
            self.threads.append(thread)
            thread.start()

    def join(self) -> None:
        # Joins the threads one by one until all of them are done.
        for thread in self.threads:
            thread.join()

    def worker(self, thread: Thread) -> None:
        # While we are running and there are functions to call:
        while self.running and (len(self.functions) > 0):
            # Get a function
            with self.functions_lock:
                function, args = self.functions.pop(0)
            # Call that function
            function(*args, threader=self)

        # Remove the thread from the list of threads.
        # This may cause issues if the user calls `<Threader>.join()`
        # But I haven't seen this problem while testing/using it.
        with self.thread_lock:
            self.threads.remove(thread)


start = perf_counter()
# I didn't need a timeout of 1 so I used 0.1
socket.setdefaulttimeout(0.2)


def connect(hostname, port, list_of_ips, threader: Threader):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex((hostname, port))
    with threader.print_lock:
        if result == 0:
            stderr.write(f"[{perf_counter() - start:.5f}] Found {hostname}\n")
            list_of_ips.append(hostname)


def find_airmore_ip() -> list:
    threader = Threader(10)
    found_ips = []
    for i in range(255):
        threader.append(connect, BASE_IP % i, PORT, found_ips)
    threader.start()
    threader.join()
    return found_ips


if __name__ == "__main__":
    ips = find_airmore_ip()
    print(f"[{perf_counter() - start:.5f}] Done searching")
    print(f"[{perf_counter() - start:.5f}] Found {len(ips)} IPs")
    print(f"[{perf_counter() - start:.5f}] IPs: {ips}")
    input("Press enter to exit.\n?")
