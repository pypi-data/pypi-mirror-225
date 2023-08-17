import builtins
import threading

lock = threading.Lock()


def sync_print(content):
    lock.acquire()
    print(content)
    lock.release()


def print(content):
    builtins.print(content)
