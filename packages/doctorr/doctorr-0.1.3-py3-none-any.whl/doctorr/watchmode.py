import time
from threading import Timer

from watchdog.events import FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer

from doctorr.utils import _get


def debounce(wait):
    """Decorator that will postpone a functions
    execution until after wait seconds
    have elapsed since the last time it was invoked."""

    def decorator(fn):
        def debounced(*args, **kwargs):
            def call_it():
                fn(*args, **kwargs)

            try:
                debounced.t.cancel()
            except AttributeError:
                pass
            debounced.t = Timer(wait, call_it)
            debounced.t.start()

        return debounced

    return decorator


def main(func, config):
    @debounce(0.1)
    def build_doc():
        # watchdog sees more events than actually happen,
        # this makes sure it runs once
        print("rebuilding...")
        func()

    class _Watcher(FileSystemEventHandler):
        def on_modified(self, event):
            if (
                "__pycache__" in event.src_path
                or not isinstance(event, FileModifiedEvent)
                or event.src_path.split(".")[-1] not in ["py", "yaml", "yml", "jinja2"]
            ):
                return
            try:
                build_doc()
            except KeyboardInterrupt as e:
                raise e
            except Exception as e:
                # todo: improve but dont quit on syntax error
                print(e)

    event_handler = _Watcher()
    observer = Observer()
    for path in _get("watch", config):
        print("watching", path)
        observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
