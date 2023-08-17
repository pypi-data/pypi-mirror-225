from pathlib import Path

ERROR_COLOR_BG = 'black'
ERROR_COLOR_FG = 'red'
TIME_SPEC = "%Y-%m-%d %H:%M:%S"

DEFAULT_STIM_PARAMS = {'stim_shape': 'BIPHASIC',
                       'stim_polarity': 'CATHODIC_FIRST',
                       'first_phase_duration_us': 100,
                       'second_phase_duration_us': 100,
                       'interphase_delay_us': 100,
                       'first_phase_amplitude_uA': 0,
                       'second_phase_amplitude_uA': 0,
                       'baseline_voltage': 0,
                       'trigger_edge_or_level': 'ST_EDGE',
                       'trigger_high_or_low': 'ST_HIGH',
                       'enabled': False,
                       'post_trigger_delay_us': 0,
                       'pulse_or_train': 'SINGLE_PULSE',
                       'number_of_stim_pulses': 2,
                       'pulse_train_period_us': 10000,
                       'refactory_period_ms': 1,
                       'pre_stim_amp_settle_us': 0,
                       'post_stim_amp_settle_us': 0,
                       'maintain_amp_settle_us': False,
                       'enable_amp_settle': False,
                       'post_stim_charge_recovery_on_us': 0,
                       'post_stim_charge_recovery_off_us': 0,
                       'enable_charge_recovery': False,
                       'trigger_source_is_keypress': False,
                       'trigger_source_idx': 0}
