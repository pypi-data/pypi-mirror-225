PRODUCT_TYPES = {
    0: "product_type_controller_home",
    1: "product_type_controller_street_lights",
    3: "product_type_inverter",
    4: "product_type_integrated_inverter_controller",
    5: "product_type_mains_frequency_off_grid",
    "default_key": "product_type_unknown"
}

SITE_CODES = {
    0: "site_code_shenzhen",
    1: "site_code_dongguan",
    "default_key": "site_code_unknown"
}

CHARGE_STATUS = {
    0: "charge_status_charging_off",
    1: "charge_status_start_charge",
    2: "charge_status_mppt_charge",
    3: "charge_status_equalizing_charge",
    4: "charge_status_boost_charge",
    5: "charge_status_floating_charge",
    6: "charge_status_over_power",
    "default_key": "charge_status_unknown"
}

LOAD_STATUS = {
    0: "load_status_off",
    1: "load_status_on",
    "default_key": "load_status_unknown"
}

ALARM_MESSAGES = {
    30: "alarm_message_charge_mos_short",
    29: "alarm_message_b2b_mos_short",
    28: "alarm_message_pv_panel_reversed_polarity",
    27: "alarm_massage_pv_panel_operating_point_over_voltage",
    26: "alarm_massage_pv_panel_counter_current",
    25: "alarm_massage_pv_input_end_over_voltage",
    24: "alarm_massage_pv_input_end_short_circuit",
    23: "alarm_massage_pv_input_power_too_high",
    22: "alarm_massage_external_temperature_too_high",
    21: "alarm_massage_controller_temperature_too_high",
    20: "alarm_massage_load_power_too_high_or_over_current",
    19: "alarm_massage_load_short_circuit",
    18: "alarm_massage_under_voltage",
    17: "alarm_massage_battery_over_voltage",
    16: "alarm_massage_battery_over_discharge",
    "default_key": "alarm_message_unknown"
}

MACHINE_STATES = {
    0: "machine_state_power_up_delay",
    1: "machine_state_waiting",
    2: "machine_state_initialization",
    3: "machine_state_soft_start",
    4: "machine_state_mains_powered_operation",
    5: "machine_state_inverter_powered_operation",
    6: "machine_state_inverter_to_mains",
    7: "machine_state_mains_to_inverter",
    10: "machine_state_shutdown",
    11: "machine_state_fault",
    "default_key": "machine_state_unknown"
}

PASSWORD_PROTECTION_STATUS_MARKS = {
    0: "password_protection_status_mark_no_user_password.",
    1: "password_protection_status_mark_user_password",
    4: "password_protection_status_mark_manufacturer_password",
    "default_key": "password_protection_status_mark_unknown"
}

SYSTEM_VOLTAGE_SETUP = {
    0x12: "system_voltage_12_volts",
    0x24: "system_voltage_24_volts",
    0x36: "system_voltage_36_volts",
    0x48: "system_voltage_48_volts",
    "default_key": "system_voltage_auto_identification"
}

DC_LOAD_WORKING_MODES = {
    0x0: "dc_load_working_mode_on_by_light_off_by_light",
    0x1: "dc_load_working_mode_on_by_light_off_after_one_hour",
    0x2: "dc_load_working_mode_on_by_light_off_after_two_hours",
    0x3: "dc_load_working_mode_on_by_light_off_after_three_hours",
    0x4: "dc_load_working_mode_on_by_light_off_after_four_hours",
    0x5: "dc_load_working_mode_on_by_light_off_after_five_hours",
    0x6: "dc_load_working_mode_on_by_light_off_after_six_hours",
    0x7: "dc_load_working_mode_on_by_light_off_after_seven_hours",
    0x8: "dc_load_working_mode_on_by_light_off_after_eight_hours",
    0x9: "dc_load_working_mode_on_by_light_off_after_nine_hours",
    0xA: "dc_load_working_mode_on_by_light_off_after_ten_hours",
    0xB: "dc_load_working_mode_on_by_light_off_after_eleven_hours",
    0xC: "dc_load_working_mode_on_by_light_off_after_twelve_hours",
    0xD: "dc_load_working_mode_on_by_light_off_after_thirteen_hours",
    0xE: "dc_load_working_mode_on_by_light_off_after_fourteen_hours",
    0xF: "dc_load_working_mode_manual",
    0x10: "dc_load_working_mode_test",
    0x11: "dc_load_working_mode_steady_on",
    "default_key": "dc_load_working_mode_unknown"
}

OUTPUT_PRIORITIES = {
    0: "output_priority_solar",
    1: "output_priority_line",
    2: "output_priority_sbu",
    "default_key": "output_priority_unknown"
}

AC_INPUT_RANGES = {
    0: "ac_input_range_wide",
    1: "ac_input_range_narrow",
    "default_key": "ac_input_range_unknown"
}

ENABLE_DISABLE = {
    0: "state_disable",
    1: "state_enable",
    "default_key": "state_unknown"
}

CHARGE_PRIORITY = {
    0: "charge_priority_pv_preferred",
    1: "charge_priority_mains_preferred",
    2: "charge_priority_hybrid",
    3: "charge_priority_pv_only",
    "default_key": "charge_priority_unknown"
}

MODBUS_ERROR_CODES = {
    0x1: ("Illegal command",
          "When the command code received from the upper computer is an impermissible operation, this may be because the function code is only applicable to new device and is not implemented in this device; in addition, it may also be that the slave processes the request in an error state."),
    0x2: ("Illegal data address",
          "For an inverter, the request data address of the upper computer is a unauthorized address; in particular, the combination of the register address and the number of transmitted bytes is invalid."),
    0x3: ("Illegal data value",
          "When the received data domain contains an impermissible value. This value indicates an error in the remaining structure in the combined request. Note: It in no way means that the data items being submitted for storage in the register have a value other than what the application expects."),
    0x4: ("Operation failed",
          "During parameter write operation, the parameter is set to be invalid; for example, the function input terminal cannot be set repeatedly."),
    0x5: ("Password error",
          "The password written at the password check address is different from the password set by the user of register 0x1305."),
    0x6: ("Data frame error",
          "When the length of data frame is incorrect or RTU format CRC bits are different from the check calculation number of lower computer in frame information sent by the upper computer"),
    0x7: ("Parameter is read only",
          "The parameters changed in the upper computer write operation are read-only parameters."),
    0x8: ("Parameter cannot be changed during running",
          "The parameters changed in the upper computer write operation are the parameters that cannot be changed during running."),
    0x9: ("Password protection"
          "When the upper computer reads or writes, if user password is set while password is not unlocked, it will report that system is locked."),
    0xA: ("Length error",
          "The number of registers required to read during the read process exceeds 12. The number of register data issued during writing exceeds 12"),
    0xB: ("Permission denied",
          "No enough permissions to do this operation"),
    "default_key": ("Unknown error",
                    "Error code is not listed in the official documentation.")
}