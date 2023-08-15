import threading

class LoadContext(threading.local):
    def __init__(self) -> None: ...
    def set_load_options(self, load_options) -> None: ...
    def clear_load_options(self) -> None: ...
    def load_options(self): ...
    def in_load_context(self): ...

def load_context(load_options) -> None: ...
def get_load_options(): ...
def in_load_context(): ...
