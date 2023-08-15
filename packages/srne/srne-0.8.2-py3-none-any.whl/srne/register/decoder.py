from typing import Any, Dict, List

from datetime import datetime

from ..tools import from_dictionary, split16
from .. import constants

def decode_default(values: List[int], scale: float) -> Any:
    values = [round(value * scale, 2) for value in values]
    len_values = len(values)
    if len_values == 0:
        return None
    elif len_values == 1:
        return values[0]
    else:
        return values
    
def decode_string(values: List[int], scale: float) -> str:
    return "".join(map(lambda x:chr(x & 0xFF), values))

def decode_datetime(values: List[int], scale: float) -> str:
    year, month = split16(values[0])
    day, hour = split16(values[1])
    minute = 0
    second = 0
    if len(values) > 2:
        minute, second = split16(values[2])
    dt = datetime(year + 2000, month, day, hour, minute, second)
    return dt.isoformat()

def decode_version(values: List[int], scale: float) -> str:
    v1, v2 = map(lambda x: x/100, values)
    if v2 > 0:
        return f"V{v1:.2f}, V{v2:.2f}"
    else:
        return f"V{v1:.2f}"

def decode_short(values: List[int], scale: float) -> int:
    value = values[0]
    if value > 32768:
        value = value - 65535
    return round(value * scale, 2)

def decode_charge_current(values: List[int], scale: float) -> int:
    return round(decode_short(values, scale) * -1, 2)

def decode_load_and_charge_status(values: List[int], scale: float) -> Dict[str, Any]:
    high, low = split16(values[0])
    load_bit = high >> 7
    brightness_bits = high & 0x7F
    status = {}
    status["charge_status"] = from_dictionary(constants.CHARGE_STATUS, low)
    status["load_status"] = from_dictionary(constants.LOAD_STATUS, load_bit)
    status["brightness_level"] = brightness_bits
    return status

def decode_alarm_message(values: List[int], scale: float) -> List[str]:
    fault_bits = values[0] << 16 | values[1]
    if fault_bits == 0:
        return []
    messages = []
    for pos in range(32):
        if fault_bits & (1 << pos):
            messages.append(from_dictionary(constants.ALARM_MESSAGES, pos))
    return messages

def decode_controller_and_battery_temperature(values: List[int], scale: float) -> Dict[str, int]:
    high, low = split16(values[0])
    temperatures = {
        "controller_temperature": high,
        "battery_temperature": low
    }
    return temperatures

def decode_current_fault_bits(values: List[int], scale: float) -> int:
    fault_bits = values[0] << 48 | values[1] << 32 | values[2] << 16 | values[3]
    if fault_bits == 0:
        return 0
    faults = 0
    for pos in range(64):
        if fault_bits & (1 << pos):
            faults += 1
    return faults

def decode_charge_discharge_cutoff_soc(values: List[int], scale: float) -> Dict[str, int]:
    high, low = split16(values[0])
    cutoff_soc = {
        "charge_cut_off_soc": high,
        "discharge_cut_off_soc": low
    }
    return cutoff_soc

def decode_special_power_control(values: List[int], scale: float) -> Dict[str, Any]:
    bits = values[0]
    load_auto_off_at_night = bool(bits & (1 << 8))
    battery_heating = bool(bits & (1 << 3))
    no_charging_below_zero = bool(bits & (1 << 2))
    charging_mode = "pwm_charging" if bits & 1 else "direct_charging"
    special_power_control = {
        "load_auto_off_at_night": load_auto_off_at_night,
        "battery_heating": battery_heating,
        "no_charging_below_zero": no_charging_below_zero,
        "charging_mode": charging_mode
    }
    return special_power_control

def decode_record(values: List[int], scale: float) -> Dict[str, Any]:
    if not any(values):
        return "no_record"
    validity = "valid_record" if values[0] else "invalid_record"
    timestamp = decode_datetime(values[1:4], 1)
    packets = values[4:]
    record = {
        "validity": validity,
        "timestamp": timestamp,
        "packets": packets
    }
    return record

def decode_machine_state(values: List[int], scale: float) -> str:
    return from_dictionary(constants.MACHINE_STATES, values[0])

def decode_password_protection_status_mark(values: List[int], scale: float) -> str:
    return from_dictionary(constants.PASSWORD_PROTECTION_STATUS_MARKS, values[0])

def decode_product_type(values: List[int], scale: float) -> str:
    return from_dictionary(constants.PRODUCT_TYPES, values[0])

def decode_site_code(values: List[int], scale: float) -> str:
    return from_dictionary(constants.SITE_CODES, values[0])

def decode_dc_load_working_mode(values: List[int], scale: float) -> str:
    return from_dictionary(constants.DC_LOAD_WORKING_MODES, values[0])

def decode_system_voltage_setup(values: List[int], scale: float) -> str:
    return from_dictionary(constants.SYSTEM_VOLTAGE_SETUP, values[0])

def decode_output_priority(values: List[int], scale: float) -> str:
    return from_dictionary(constants.OUTPUT_PRIORITIES, values[0])

def decode_ac_input_range(values: List[int], scale: float) -> str:
    return from_dictionary(constants.AC_INPUT_RANGES, values[0])

def decode_enable_disable(values: List[int], scale: float) -> str:
    return from_dictionary(constants.ENABLE_DISABLE, values[0])

def decode_charge_priority(values: List[int], scale: float) -> str:
    return from_dictionary(constants.CHARGE_PRIORITY, values[0])
