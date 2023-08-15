from typing import Any, Dict, Callable, List

from . import decoder


class Register:

    def __init__(self,
                 address: int,
                 length: int = 1,
                 name: str = "Reserved",
                 access: str = "r",
                 scale: float = 1,
                 unit: str = "",
                 decoder: Callable = decoder.decode_default,
                 encoder: Callable = None,
                 partition: str = "") -> None:
        self.address = address
        self.length = length
        self.name = name
        self.access = access
        self.scale = scale
        self.unit = unit
        self.decoder = decoder
        self.encoder = encoder
        self.partition = partition

    def __repr__(self) -> str:
        return f"Register({hex(self.address)})"

    def format_value(self, raw_value: List[int] = []) -> Any:
        if not len(raw_value):
            return "decoder_received_no_value"
        scaled = [round(value * self.scale, 2) for value in raw_value]
        try:
            formatted = self.decoder(scaled)
        except:
            formatted = "decoder_failure"
        return formatted

    def serialize(self, raw_value: List[int] = []) -> Dict[str, Any]:
        result = {
            "address": hex(self.address),
            "length": self.length,
            "name": self.name,
            "access": self.access,
            "unit": self.unit,
            "decoder": self.decoder.__name__,
            "partition": self.partition,
        }
        if len(raw_value):
            result["value"] = self.format_value(raw_value)
            result["raw_value"] = raw_value
        return result
