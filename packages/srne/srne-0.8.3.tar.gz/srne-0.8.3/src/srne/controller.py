import asyncio
from typing import Any, Dict, List, overload

from .register import Register
from .register.factory import RegisterFactory
from .register.sequencer import RegisterSequencer

from .modbus import ModBus


class Controller:

    def __init__(self,
                 executor_address: int = 0x0,
                 serial_port: str = "/dev/ttyUSB0",
                 baudrate: int = 9600,
                 bytesize: int = 8,
                 stopbits: int = 1,
                 timeout: int = 3,
                 dummy: int = False) -> None:
        self.modbus = ModBus(executor_address, serial_port, baudrate, bytesize, stopbits, timeout, dummy)
        self.registers: List[Register] = []
        self.register_sequences: List[List[int]] = []

    def filter_registers(self,
                         register_filter: Dict[str, List[str]] = {"access": ["r", "rw"]},
                         sequencer_max_len: int = 20) -> None:
        """NOTE: Avoid filtering for write-only registers. Reading those will
                 only return zeros and may pose risks to your device."""
        self.registers = RegisterFactory.get_registers(register_filter)
        self.register_sequences = RegisterSequencer.get_register_sequences(self.registers, sequencer_max_len)
    
    def readout(self):
        return self.modbus.read_register_sequences(self.register_sequences)

    def get_register_values(self) -> Dict[Register, List[int]]:
        """Return a python dictionary of the filtered registers and their
           current values."""
        readout = self.readout()
        return RegisterSequencer.fetch_register_values(self.registers, readout)
    
    def serialize(self) -> Dict[str, Dict[str, Any]]:
        """Return a JSON string of the filtered registers serialized with their
           current values."""
        register_values = self.get_register_values()
        return {r.name: r.serialize(v) for r, v in register_values.items()}

    def read_registers(self, registers: List[Any], sequencer_max_len: int = 20) -> Dict[Register, List[int]]:
        _registers = [RegisterFactory.get_register(register) for register in registers]
        _sequences = RegisterSequencer.get_register_sequences(_registers, sequencer_max_len)
        readout = self.modbus.read_register_sequences(_sequences)
        return RegisterSequencer.fetch_register_values(_registers, readout)

    @overload
    def read_register(self, name: str) -> Dict[str, Any]:
        ...

    @overload
    def read_register(self, address: int) -> Dict[str, Any]:
        ...

    def read_register(self, register) -> Dict[str, Any]:
        """
        Returns:
        ```python
        {"register": register, "response": response}
        ```
        """
        _register = RegisterFactory.get_register(register)
        response = self.modbus.read_holding_registers(_register.address, _register.length)
        return {"register": _register, "response": response}

    @overload
    def write_register(self, name: str, values: List[int]) -> Dict[str, Any]:
        ...
    
    @overload
    def write_register(self, address: int, values: List[int]) -> Dict[str, Any]:
        ...
    
    def write_register(self, register, values: List[int]) -> Dict[str, Any]:
        """
        Returns:
        ```python
        {"register": register, "response": response}
        ```
        """
        _register = RegisterFactory.get_register(register)
        response = self.modbus.write_multiple_register(_register.address, values)
        return {"register": _register, "response": response}


class AsyncController(Controller):

    def __init__(self,
                 executor_address: int = 0,
                 serial_port: str = "/dev/ttyUSB0",
                 baudrate: int = 9600,
                 bytesize: int = 8,
                 stopbits: int = 1,
                 timeout: int = 3,
                dummy: int = False) -> None:
        super().__init__(executor_address, serial_port, baudrate, bytesize, stopbits, timeout, dummy)
        self.modbus_lock = asyncio.Lock()
    
    async def _read_sequences_async(self, sequences) -> Dict[int, List[int]]:
        readout = {}
        for address, length in sequences:
            async with self.modbus_lock:
                readout[address] = self.modbus.read_holding_registers(address, length).values
            await asyncio.sleep(self.modbus.character_time * 3.5)
        return readout

    async def readout(self):
        _readout = await self._read_sequences_async(self.register_sequences)
        return _readout

    async def get_register_values(self) -> Dict[Register, List[int]]:
        readout = await self.readout()
        return RegisterSequencer.fetch_register_values(self.registers, readout)

    async def serialize(self) -> Dict[str, Dict[str, Any]]:
        register_values = await self.get_register_values()
        return {r.name: r.serialize(v) for r, v in register_values.items()}

    async def read_registers(self, registers: List[Any], sequencer_max_len: int = 20) -> Dict[Register, List[int]]:
        _registers = [RegisterFactory.get_register(register) for register in registers]
        _sequences = RegisterSequencer.get_register_sequences(_registers, sequencer_max_len)
        readout = await self._read_sequences_async(_sequences)
        return RegisterSequencer.fetch_register_values(_registers, readout)

    async def read_register(self, register) -> Dict[str, Any]:
        _register = RegisterFactory.get_register(register)
        async with self.modbus_lock:
            response = self.modbus.read_holding_registers(_register.address, _register.length)
        return {"register": _register, "response": response}

    async def write_register(self, register, values: List[int]) -> Dict[str, Any]:
        _register = RegisterFactory.get_register(register)
        async with self.modbus_lock:
            response = self.modbus.write_multiple_register(_register.address, values)
        return {"register": _register, "response": response}
