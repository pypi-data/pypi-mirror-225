from typing import Union, Any

class PyperclipException(RuntimeError): ...

class PyperclipWindowsException(PyperclipException):
    def __init__(self, message) -> None: ...

class CheckedCall:
    def __init__(self, f) -> None: ...
    def __call__(self, *args): ...
    def __setattr__(self, key, value) -> None: ...

def determine_clipboard(): ...
def set_clipboard(clipboard) -> None: ...

copy: Any
paste: Any
clipboard_get = paste
clipboard_set = copy
