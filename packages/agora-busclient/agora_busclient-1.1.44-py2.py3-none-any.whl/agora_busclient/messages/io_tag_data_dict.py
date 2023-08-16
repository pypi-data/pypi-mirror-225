from .io_point import IoPoint
from typing import Dict

class IoTagDataDict(Dict[str, IoPoint]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __setitem__(self, key: str, value: IoPoint):
        if not isinstance(value, IoPoint):
            raise ValueError("Value must be an instance of IoPoint")
        super().__setitem__(key, value)