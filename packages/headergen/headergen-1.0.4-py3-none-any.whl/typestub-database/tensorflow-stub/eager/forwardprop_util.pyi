from tensorflow.python import pywrap_tfe as pywrap_tfe
from typing import Any

class TangentInfo:
    def __new__(cls, indices: Any | None = ..., tangents: Any | None = ...): ...

def pack_tangents(tensors): ...
def push_forwardprop_state() -> None: ...
