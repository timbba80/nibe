nibe_registers = {
    0: "nibe/cpu_id",
    1: "nibe/outdoor_temp_c",  
    4: "nibe/heating_curve",
    5: "nibe/flow_setpoint_c",  
    6: "nibe/flow_actual_c",  
    7: "nibe/return_temp_c",
    8: "nibe/degree_minutes",
    12: "nibe/domestic_hot_water_top_temp",
    25: "nibe/compressor_starts",
    31: "nibe/heating_status",
    32: "nibe/additional_heating_allowed",
    33: "nibe/max_df_compressor",
    34: "nibe/verd_freq_reg_p",
    35: "nibe/min_start_time_freq_min",
    36: "nibe/min_time_const_freq_min",
    38: "nibe/comp_freq_grad_min",
    44: "nibe/pump_speed_percent",
    45: "nibe/bw_reg_p",
    46: "nibe/bw_reg_q",
    48: "nibe/bw_reg_value_xp_percent",
    100: "nibe/date_year",
    101: "nibe/date_month",
    102: "nibe/date_day",
    103: "nibe/time_hour",
    104: "nibe/time_minute",
    105: "nibe/time_second",
    24: "nibe/run_time_compressor_h",
    9: "nibe/comp_freq_desired_hz",
    10: "nibe/comp_freq_actual_hz",
    19: "nibe/high_pressure_bar",
    20: "nibe/low_pressure_bar",
    22: "nibe/ams_phase_is_a",
    40: "nibe/hysteresis",
    47: "nibe/bw_reg_xp",
    43: "nibe/stop_temp_heating_c",
    49: "nibe/domestic_hot_water_start_temp",
    50: "nibe/domestic_hot_water_stop_temp",
    28: "nibe/operation_mode_reg_28",
    29: "nibe/operation_mode_reg_29",
    30: "nibe/operation_mode_reg_30",
    23: "nibe/inverter_temp_tho_ip",
    11: "nibe/condenser_off_max",
    13: "nibe/domestic_hot_water_bottom",
    14: "nibe/tho_r1_evap_temp",
    15: "nibe/tho_r2_evap_temp",
    16: "nibe/suction_gas_temp_tho_s",
    17: "nibe/hot_gas_temp_tho_d",
    18: "nibe/liquid_temp_ams",
    21: "nibe/resp_at_ams_tho_a",
}
  

# Define unique IDs and MQTT discovery configurations for each sensor
mqtt_discovery_sensors = {
    "nibe/pump_speed_percent": {
        "name": "Pump Speed Percent",
        "unit_of_measurement": "%",
        "state_topic": "nibe/pump_speed_percent",
        "unique_id": "nibe_pump_speed_percent"
    },
#    "nibe/cpu_id": {
#        "name": "CPU ID",
#        "state_topic": "nibe/cpu_id",
#        "unique_id": "nibe_cpu_id"
#    },
    "nibe/inverter_temp_tho_ip": {
        "name": "Inverter temp Tho-IP",
        "state_class": "measurement",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "state_topic": "nibe/inverter_temp_tho_ip",
        "unique_id": "nibe_inverter_temp_tho_ip"
    },
    "nibe/operation_mode": {
        "name": "Nibe Operation Mode",
        "state_topic": "nibe/operation_mode",
    "unique_id": "nibe_operation_mode"
    },
    "nibe/condenser_off_max": {
        "name": "Condenser Off (MAX)",
        "state_topic": "nibe/condenser_off_max",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "unique_id": "nibe_condenser_off_max"
    },
    "nibe/domestic_hot_water_bottom": {
        "name": "Domestic Hot Water Bottom",
        "state_topic": "nibe/domestic_hot_water_bottom",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "unique_id": "nibe_domestic_hot_water_bottom"
    },
    "nibe/tho_r1_evap_temp": {
        "name": "Tho-R1 Evaporator Temp",
        "state_topic": "nibe/tho_r1_evap_temp",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "unique_id": "nibe_tho_r1_evap_temp"
    },
    "nibe/tho_r2_evap_temp": {
        "name": "Tho-R2 Evaporator Temp",
        "state_topic": "nibe/tho_r2_evap_temp",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "unique_id": "nibe_tho_r2_evap_temp"
    },
    "nibe/suction_gas_temp_tho_s": {
        "name": "Suction Gas Temp Tho-S",
        "state_topic": "nibe/suction_gas_temp_tho_s",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "unique_id": "nibe_suction_gas_temp_tho_s"
    },
    "nibe/hot_gas_temp_tho_d": {
        "name": "Hot Gas Temp Tho-D",
        "state_topic": "nibe/hot_gas_temp_tho_d",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "unique_id": "nibe_hot_gas_temp_tho_d"
    },
    "nibe/liquid_temp_ams": {
        "name": "Liquid Temp AMS",
        "state_topic": "nibe/liquid_temp_ams",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "unique_id": "nibe_liquid_temp_ams"
    },
    "nibe/resp_at_ams_tho_a": {
        "name": "Response at AMS Tho-A",
        "state_topic": "nibe/resp_at_ams_tho_a",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "unique_id": "nibe_resp_at_ams_tho_a"
    },     
    "nibe/heating_curve": {
        "name": "Heating Curve",
        "state_topic": "nibe/heating_curve",
        "state_class": "measurement",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_heating_curve"
    },
    "nibe/return_temp_c": {
        "name": "Return Temperature",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "state_topic": "nibe/return_temp_c",
        "unique_id": "nibe_return_temp_c"
    },
    "nibe/degree_minutes": {
        "name": "Degree Minutes",
        "state_topic": "nibe/degree_minutes",
        "state_class": "measurement",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_degree_minutes"
    },
    "nibe/domestic_hot_water_top_temp": {
        "name": "Domestic Hot Water Top Temperature",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "state_topic": "nibe/domestic_hot_water_top_temp",
        "unique_id": "nibe_domestic_hot_water_top_temp"
    },
    "nibe/max_df_compressor": {
        "name": "Max DF Compressor",
        "state_topic": "nibe/max_df_compressor",
        "unit_of_measurement": "Hz",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_max_df_compressor"
    },
    "nibe/verd_freq_reg_p": {
        "name": "Verd Freq Reg P",
        "state_topic": "nibe/verd_freq_reg_p",
        "unit_of_measurement": "Hz",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_verd_freq_reg_p"
    },
    "nibe/min_start_time_freq_min": {
        "name": "Min Start Time Freq Min",
        "unit_of_measurement": "Hz",
        "state_topic": "nibe/min_start_time_freq_min",
        "unique_id": "nibe_min_start_time_freq_min"
    },
    "nibe/min_time_const_freq_min": {
        "name": "Min Time Const Freq Min",
        "state_topic": "nibe/min_time_const_freq_min",
        "unit_of_measurement": "Hz",
        "unique_id": "nibe_min_time_const_freq_min"
    },
    "nibe/comp_freq_grad_min": {
        "name": "Comp Freq Grad Min",
        "state_topic": "nibe/comp_freq_grad_min",
        "unit_of_measurement": "Hz",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_comp_freq_grad_min"
    },
    "nibe/bw_reg_p": {
        "name": "BW Reg P",
        "state_topic": "nibe/bw_reg_p",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_bw_reg_p"
    },
    "nibe/bw_reg_q": {
        "name": "BW Reg Q",
        "state_topic": "nibe/bw_reg_q",
        "value_template": "{{ value | float }}",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "unique_id": "nibe_bw_reg_q"
    },
    "nibe/bw_reg_value_xp_percent": {
        "name": "BW Reg Value XP Percent",
        "unit_of_measurement": "%",
        "state_topic": "nibe/bw_reg_value_xp_percent",
        "unique_id": "nibe_bw_reg_value_xp_percent"
    },

#enable if you want mqtt to publish time and date
#    "nibe/date_year": {
#        "name": "Date Year",
#        "state_topic": "nibe/date_year",
#        "unique_id": "nibe_date_year"
#    },
#    "nibe/date_month": {
#        "name": "Date Month",
#        "state_topic": "nibe/date_month",
#        "unique_id": "nibe_date_month"
#    },
#    "nibe/date_day": {
#        "name": "Date Day",
#        "state_topic": "nibe/date_day",
#        "unique_id": "nibe_date_day"
#    },
#    "nibe/time_hour": {
#        "name": "Time Hour",
#        "state_topic": "nibe/time_hour",
#        "unique_id": "nibe_time_hour"
#    },
#    "nibe/time_minute": {
#        "name": "Time Minute",
#        "state_topic": "nibe/time_minute",
#        "unique_id": "nibe_time_minute"
#    },
#    "nibe/time_second": {
#        "name": "Time Second",
#        "state_topic": "nibe/time_second",
#        "unique_id": "nibe_time_second"
#    },
    "nibe/run_time_compressor_h": {
        "name": "Run Time Compressor Hours",
        "state_topic": "nibe/run_time_compressor_h",
        "device_class": "duration",
        "unit_of_measurement": "h",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_run_time_compressor_h"
    },
    "nibe/comp_freq_desired_hz": {
        "name": "Comp Freq Desired Hz",
        "unit_of_measurement": "Hz",
        "state_topic": "nibe/comp_freq_desired_hz",
        "unique_id": "nibe_comp_freq_desired_hz"
    },
    "nibe/comp_freq_actual_hz": {
        "name": "Comp Freq Actual Hz",
        "unit_of_measurement": "Hz",
        "state_topic": "nibe/comp_freq_actual_hz",
        "unique_id": "nibe_comp_freq_actual_hz"
    },
    "nibe/high_pressure_bar": {
        "name": "High Pressure Bar",
        "unit_of_measurement": "bar",
        "state_topic": "nibe/high_pressure_bar",
        "unique_id": "nibe_high_pressure_bar"
    },
    "nibe/low_pressure_bar": {
        "name": "Low Pressure Bar",
        "unit_of_measurement": "bar",
        "state_topic": "nibe/low_pressure_bar",
        "unique_id": "nibe_low_pressure_bar"
    },
    "nibe/ams_phase_is_a": {
        "name": "AMS Phase Current",
        "unit_of_measurement": "A",
        "state_topic": "nibe/ams_phase_is_a",
        "unique_id": "nibe_ams_phase_is_a"
    },
    "nibe/hysteresis": {
        "name": "Hysteresis",
        "state_topic": "nibe/hysteresis",
        "state_class": "measurement",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_hysteresis"
    },
    "nibe/bw_reg_xp": {
        "name": "BW Reg XP",
        "state_topic": "nibe/bw_reg_xp",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_bw_reg_xp"
    },
    "nibe/stop_temp_heating_c": {
        "name": "Stop Temp Heating",
        "unit_of_measurement": "°C",
        "state_topic": "nibe/stop_temp_heating_c",
        "unique_id": "nibe_stop_temp_heating_c"
    },
    "nibe/domestic_hot_water_start_temp": {
        "name": "Domestic Hot Water Start Temp",
        "unit_of_measurement": "°C",
        "state_topic": "nibe/domestic_hot_water_start_temp",
        "unique_id": "nibe_domestic_hot_water_start_temp"
    },
    "nibe/domestic_hot_water_stop_temp": {
        "name": "Domestic Hot Water Stop Temp",
        "unit_of_measurement": "°C",
        "state_topic": "nibe/domestic_hot_water_stop_temp",
        "unique_id": "nibe_domestic_hot_water_stop_temp"
    },
    "nibe/outdoor_temp_c": {
        "name": "Outdoor Temperature",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "state_topic": "nibe/outdoor_temp_c",
        "unique_id": "nibe_outdoor_temp_c"
    },
    "nibe/flow_setpoint_c": {
        "name": "Flow Setpoint Temperature",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "state_topic": "nibe/flow_setpoint_c",
        "unique_id": "nibe_flow_setpoint_c"
    },
    "nibe/flow_actual_c": {
        "name": "Flow Actual Temperature",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "state_topic": "nibe/flow_actual_c",
        "unique_id": "nibe_flow_actual_c"
    },
    "nibe/compressor_starts": {
        "name": "Compressor starts",
        "state_topic": "nibe/compressor_starts",
        "unit_of_measurement": "x",
        "state_class": "total_increasing",
        "value_template": "{{ value | float }}",
        "unique_id": "nibe_compressor_starts"
    },
    "nibe/heating_status": {
        "name": "Heating Status",
        "state_topic": "nibe/heating_status",
        "unique_id": "nibe_heating_status"
    },
    "nibe/additional_heating": {
        "name": "Additional Heating Allowed",
        "state_topic": "nibe/additional_heating_allowed",
        "unique_id": "nibe_additional_heating_allowed",
        "value_template": "{{ value | int }}",  # Ensure Home Assistant interprets 0 and 1 as integers
        "availability_topic": "nibe/status",
        "payload_available": "online",
        "payload_not_available": "offline",
        "device": {
            "identifiers": ["nibe_heat_pump"],
            "name": "Nibe Heat Pump",
            "manufacturer": "Nibe",
            "model": "EasySolar",
            "sw_version": "1.0"
    }
},

}

