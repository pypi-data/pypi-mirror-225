from typing import Any, List, Dict

from . import Register


class RegisterSequencer:

    @classmethod
    def get_register_sequences(cls, registers: List[Register], max_length: int = 20) -> List[List[int]]:
        if len(registers) <= 2:
            return [[r.address, r.length] for r in registers]
        registers_groups = [[]]
        sequences = []
        registers = sorted(registers, key=lambda r: r.address)
        registers_ranges = [range(register.address, register.address + register.length) for register in registers]
        for register_range in registers_ranges:
            for a in register_range:
                if len(registers_groups[-1]) == 0:
                    registers_groups[-1].append(a)
                elif len(registers_groups[-1]) == max_length:
                    registers_groups.append([a])
                elif registers_groups[-1][-1] == a:
                    continue
                elif registers_groups[-1][-1] != a - 1:
                    registers_groups.append([a])
                else:
                    registers_groups[-1].append(a)
        for register_range in registers_groups:
            if len(register_range):
                sequences.append([register_range[0], len(register_range)])
        return sequences

    @classmethod
    def fetch_register_values(cls, registers: List[Register], readout: Dict[int, List[int]]) -> Dict[Register, List[int]]:
        register_values = {}
        for key, values in readout.items():
            address = key
            for value in values:
                for register in registers:
                    if register.address <= address < register.address + register.length:
                        try:
                            register_values[register].append(value)
                        except KeyError:
                            register_values[register] = [value]
                address += 1
        return register_values
