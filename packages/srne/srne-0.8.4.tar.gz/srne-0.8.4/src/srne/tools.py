from typing import Any, List, Tuple

def from_dictionary(dictionary : dict,
                    key,
                    default_value=None,
                    default_key="default_key") -> Any:
    try:
        return dictionary[key]
    except KeyError:
        if default_value:
            return default_value
        else:
            return dictionary[default_key]

def split16(byte: int) -> Tuple[int, int]:
    return byte >> 8, byte & 0xFF

def join16(high: int, low) -> int:
    return (high << 8) | low

def crc16(data: List[int]) -> int:
    """ Calculate CRC16
    ```python
    >>> message = [0x0, 0xB, 0x0, 0x1]
    >>> calculated_crc = crc16(message)
    >>> print(f"Calculated CRC: {hex(calculated_crc)}")    
    Calculated CRC: 0x26b0
    ```
    """
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc
