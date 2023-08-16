import struct
from time import sleep
from serial import Serial, PARITY_NONE

from typing import Any, Dict, List

from .tools import from_dictionary, crc16, split16, join16

from .constants import MODBUS_ERROR_CODES


class ModBusError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class BaseRequest:

    def __init__(self,
                 executor_address: int,
                 function_code: int,
                 register_address: int,
                 length: int) -> None:
        self.executor_address = executor_address
        self.function_code = function_code
        self.register_address = register_address
        self.length = length
        self.header = [self.executor_address, self.function_code]
        self.data = []

    def to_bytes(self) -> bytes:
        self.frame = []
        self.frame.extend(self.header)
        self.frame.extend(self.data)
        self.frame.extend(reversed(split16(crc16(self.frame))))
        return struct.pack(">" + "B" * len(self.frame), *self.frame)


class ReadHoldingRegistersRequest(BaseRequest):

    def __init__(self,
                 register_address: int,
                 length: int,
                 executor_address: int = 0x0) -> None:
        super().__init__(executor_address,
                         0x3,
                         register_address,
                         length)
        self.data.extend(split16(self.register_address))
        self.data.extend(split16(self.length))


class WriteMultipleRegistersRequest(BaseRequest):

    def __init__(self,
                 register_address: int,
                 length: int,
                 values: List[int],
                 executor_address: int = 0x0) -> None:
        super().__init__(executor_address, 0x10, register_address, length)
        self.values = values
        self.data.extend(split16(self.register_address))
        self.data.extend(split16(self.length))
        self.data.append(len(self.values)*2)
        for value in self.values:
            self.data.extend(split16(value))


class BaseResponse:
    
    def __init__(self, response) -> None:
        self.response = response

    @property
    def executor_address(self) -> int:
        return self.response[0]
    
    @property
    def function_code(self) -> int:
        return self.response[1]
    
    @property
    def data(self) -> List[int]:
        return self.response[2:-2]

    @property
    def crc(self) -> int:
        return join16(*reversed(self.response[-2:]))
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}([{', '.join(hex(r) for r in self.response)}])"


class ReadHoldingRegistersResponse(BaseResponse):
    
    @property
    def length(self) -> int:
        return self.response[2]
    
    @property
    def values(self) -> List[int]:
        return [join16(*self.response[3+i:i+5]) for i in range(0, self.length, 2)]


class WriteMultipleRegistersResponse(BaseResponse):

    @property
    def register_address(self) -> int:
        return join16(self.response[2], self.response[3])

    @property
    def length(self) -> int:
        return join16(self.response[4], self.response[5])


class ModBus:

    def __init__(self,
                 executor_address = 0x0,
                 serial_port = "/dev/ttyUSB0",
                 baudrate = 9600,
                 bytesize = 8,
                 stopbits = 1,
                 timeout = 3,
                 dummy = False) -> None:
        self.executor_address = executor_address
        self.port = serial_port
        self.dummy = dummy
        self.character_time = (bytesize + stopbits + 1) / baudrate
        self._serial = Serial(baudrate=baudrate,
                              bytesize=bytesize,
                              parity=PARITY_NONE,
                              stopbits=stopbits,
                              timeout=timeout,
                              inter_byte_timeout=self.character_time * 1.5)
        self._serial.port = self.port

    def process_request(self, request) -> Any:
        try:    
            response = []
            response_type = BaseResponse
            with self._serial as port:
                sleep(self.character_time * 3.5)
                port.write(request.to_bytes())
                response.extend(struct.unpack(">BBBBB", port.read(5)))
                function_code = response[1]
                if function_code == 0x3:
                    remaining_byte_count = response[2]
                    response_type = ReadHoldingRegistersResponse
                elif function_code == 0x10:
                    remaining_byte_count = 3
                    response_type = WriteMultipleRegistersResponse
                elif function_code == 0x83 or function_code == 0x90:
                    error_code = response[2]
                    args = from_dictionary(MODBUS_ERROR_CODES, error_code)
                    args = (f"function_code: {hex(function_code)}", *args)
                    raise ModBusError(*args)
                else:
                    args = (f"function_code: {hex(function_code)}",
                            "Response contains unknown or unimplemented function.")
                    raise ModBusError(*args)
                remaining_bytes = port.read(remaining_byte_count)
        except struct.error as e:
            ModBusError("Malformed response.", *e.args)
        finally:
            pass
        if not len(response):
            raise ModBusError("Could not read from serial port", self.port)
        response.extend(struct.unpack(">" + "B" * remaining_byte_count, remaining_bytes))
        crc = join16(*reversed(response[-2:]))  # reversed
        f_crc = crc16(response[:-2])
        if f_crc != crc:
            raise ModBusError(f"CRC mismatch! Received: {hex(crc)}, Calculated: {hex(f_crc)}")
        return response_type(response)

    def read_holding_registers(self, address: int, length: int) -> ReadHoldingRegistersResponse:
        if self.dummy:
            dummy_response = [self.executor_address, 0x3, length * 2]
            dummy_response.extend([0x1] * length * 2)
            dummy_response.extend(reversed(split16(crc16(dummy_response))))
            return ReadHoldingRegistersResponse(dummy_response)
        request = ReadHoldingRegistersRequest(address, length, self.executor_address)
        return self.process_request(request)

    def write_multiple_register(self, address: int, values: List[int]) -> WriteMultipleRegistersResponse:
        if self.dummy:
            dummy_response = [self.executor_address, 0x10]
            dummy_response.extend(split16(address))
            dummy_response.extend(split16(len(values)))
            return WriteMultipleRegistersResponse(dummy_response)
        request = WriteMultipleRegistersRequest(address, len(values), values, self.executor_address)
        return self.process_request(request)
    
    def read_register_sequences(self, register_sequences: List[List[int]]) -> Dict[int, List[int]]:
        data = {}
        for address, length in register_sequences:
            data[address] = self.read_holding_registers(address, length).values
        return data
