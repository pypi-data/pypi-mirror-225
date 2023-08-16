from typing import Dict, List, overload

from .data import REGISTER
from . import Register


class RegisterFactory:

    @classmethod
    def _get_register(cls, address: int) -> Register:
        try:
            kwargs = REGISTER[address]
        except KeyError:
            raise KeyError("No such register address.")
        return Register(address, **kwargs)

    @classmethod
    def _get_registers(cls, query: Dict[str, List[str]]) -> List[Register]:
        registers = []
        for address, data in REGISTER.items():
            try:
                match = True
                for key, value in query.items():
                    if not data[key] in value:
                        match = False
                if match:
                    registers.append(cls._get_register(address))
            except KeyError:
                pass
        if not len(registers):
            raise ValueError("Can't locate register.")
        return registers

    @classmethod
    def get_register_by_address(cls, address: int) -> Register:
        return cls._get_register(address)

    @classmethod
    def get_register_by_name(cls, name: str) -> Register:
        return cls._get_registers({"name": [name]})[0]

    @overload
    @classmethod
    def get_register(cls, address: int) -> Register:
        ...
    
    @overload
    @classmethod
    def get_register(cls, name: str) -> Register:
        ...

    @classmethod
    def get_register(cls, register) -> Register:
        if isinstance(register, str):
            return cls.get_register_by_name(register)
        elif isinstance(register, int):
            return cls.get_register_by_address(register)

    @classmethod
    def get_registers(cls, register_filter: Dict[str, List[str]]) -> List[Register]:
        """
        Not all keys are available for query.
        Multiple keys can be used as a "filter".
        See the examples in the repo, or check how keys are stored in `data.py`.
        These keys are always defined: `name`, `access`, `partition`.

        Example:
        ```python
        example_one = {"name": ["product_type", "product_model"]}
        example_two = {"partition": ["p03"]}
        example_three = {"unit": ["A", "V", "W"]}
        example_four = {"unit": ["r", "rw"]}
        ```
        """
        return cls._get_registers(register_filter)
