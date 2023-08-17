import pandas as pd

PORT_ENUM = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
SIGNAL_TYPE_ENUM = {0: 'Pri', 1: 'Aux', 2: 'Din', 3: 'Dout'}


class SignalGroup():
    '''
    Channel mapping metadata 
    '''

    def __init__(self, raw):
        """
        """
        self._df, self._sensor_spec = decode_grpc_message(raw)
        self._sigs = {}
        self._sel_sigs = {}
        for stype in ['Pri', 'Aux', 'Din', 'Dout']:
            stype2 = stype.lower()
            self._sigs[stype2] = self._df[self._df['chan_type'] == stype]
            self._sel_sigs[stype2] = self._sigs[stype2][self._sigs[stype2]['is_selected'] == True]

    @property
    def full_table(self) -> pd.DataFrame:
        """
        Dataframe describing channel metadata (index, position, channel type, units, etc)
        """
        return self._df

    @property
    def num_sigs(self) -> dict:
        """
        Dict with keys (str) ``'pri'``, ``'aux'``, ``'din'``, ``'dout'`` mapping to their respective number of signals
        """
        rv = {}
        for stype in ['pri', 'aux', 'din', 'dout']:
            rv[stype] = len(self._sigs[stype])
        return rv

    @property
    def num_selected_sigs(self) -> dict:
        """
        Dict with keys (str) ``'pri'``, ``'aux'``, ``'din'``, ``'dout'`` mapping to their respective number of selected signals
        """
        rv = {}
        for stype in ['pri', 'aux', 'din', 'dout']:
            rv[stype] = len(self._sel_sigs[stype])
        return rv

    @property
    def sensor_spec(self) -> dict:
        """
        Dict with ports (str) as keys mapping to dicts describing headstage, site, and probe wireframe metadata
        """
        return self._sensor_spec

    def sigs(self, signal_type):
        """
        Parameters:
            signal_type (str): one of ``'pri'``, ``'aux'``, ``'din'``, or ``'dout'`` 
        Returns: 
            sigs (dict): full_table but just for ``signal_type``
        """
        if signal_type.lower() not in ['pri', 'aux', 'din', 'dout']:
            raise ValueError('invalid signal_type parameter')
        return self._sigs[signal_type.lower()]

    def selected_sigs(self, signal_type):
        """
        Parameters:
            signal_type (str): one of ``'pri'``, ``'aux'``, ``'din'``, or ``'dout'`` 
        Returns: 
            sel_sigs (dict): full_table but just for ``signal_type`` of selected sigs
        """
        if signal_type.lower() not in ['pri', 'aux', 'din', 'dout']:
            raise ValueError('invalid signal_type parameter')
        return self._sel_sigs[signal_type.lower()]


def decode_grpc_message(raw_grpc):
    chan_name = []
    chan_type = []
    ntv_chan_idx = []
    site_num = []
    color_group_idx = []
    is_selected = []
    is_audio_left = []
    is_audio_right = []
    port = []
    site_shape = []
    site_ctr_x = []
    site_ctr_y = []
    site_ctr_z = []
    site_lim_x_min = []
    site_lim_y_min = []
    site_lim_z_min = []
    site_lim_x_max = []
    site_lim_y_max = []
    site_lim_z_max = []
    site_ctr_tcs_x = []
    site_ctr_tcs_y = []
    site_ctr_tcs_z = []
    sensor_units = []
    abs_idx = []
    for row in raw_grpc.channels:
        chan_name.append(row.chanName)
        chan_type.append(SIGNAL_TYPE_ENUM[row.chanType])
        ntv_chan_idx.append(row.ntvChanIdx)
        site_num.append(row.siteNum)
        color_group_idx.append(row.colorGroupIdx)
        is_selected.append(row.isSelected)
        is_audio_left.append(row.isAudioLeft)
        is_audio_right.append(row.isAudioRight)
        port.append(PORT_ENUM[row.port])
        site_shape.append(row.siteShape)
        site_ctr_x.append(row.siteCtrX)
        site_ctr_y.append(row.siteCtrY)
        site_ctr_z.append(row.siteCtrZ)
        site_lim_x_min.append(row.siteLimXMin)
        site_lim_y_min.append(row.siteLimYMin)
        site_lim_z_min.append(row.siteLimZMin)
        site_lim_x_max.append(row.siteLimXMax)
        site_lim_y_max.append(row.siteLimYMax)
        site_lim_z_max.append(row.siteLimZMax)
        site_ctr_tcs_x.append(row.siteCtrTcsX)
        site_ctr_tcs_y.append(row.siteCtrTcsY)
        site_ctr_tcs_z.append(row.siteCtrTcsZ)
        sensor_units.append(row.sensorUnits)
        abs_idx.append(row.absIdx)

    _df = pd.DataFrame({'chan_name': chan_name,
                        'chan_type': chan_type,
                        'ntv_chan_idx': ntv_chan_idx,
                        'site_num': site_num,
                        'color_group_idx': color_group_idx,
                        'is_selected': is_selected,
                        'is_audio_left': is_audio_left,
                        'is_audio_right': is_audio_right,
                        'port': port,
                        'site_shape': site_shape,
                        'site_ctr_x': site_ctr_x,
                        'site_ctr_y': site_ctr_y,
                        'site_ctr_z': site_ctr_z,
                        'site_lim_x_min': site_lim_x_min,
                        'site_lim_y_min': site_lim_y_min,
                        'site_lim_z_min': site_lim_z_min,
                        'site_lim_x_max': site_lim_x_max,
                        'site_lim_y_max': site_lim_y_max,
                        'site_lim_z_max': site_lim_z_max,
                        'site_ctr_tcs_x': site_ctr_tcs_x,
                        'site_ctr_tcs_y': site_ctr_tcs_y,
                        'site_ctr_tcs_z': site_ctr_tcs_z,
                        'sensor_units': sensor_units,
                        'abs_idx': abs_idx
                        })

    sensor_port_spec = {}
    if len(raw_grpc.sensorPortSpec.sensorA.probeId) > 0:
        sensor_port_spec['A'] = decode_grpc_sensor_port_spec(raw_grpc.sensorPortSpec.sensorA)
    else:
        sensor_port_spec['A'] = None

    if len(raw_grpc.sensorPortSpec.sensorB.probeId) > 0:
        sensor_port_spec['B'] = decode_grpc_sensor_port_spec(raw_grpc.sensorPortSpec.sensorB)
    else:
        sensor_port_spec['B'] = None

    if len(raw_grpc.sensorPortSpec.sensorC.probeId) > 0:
        sensor_port_spec['C'] = decode_grpc_sensor_port_spec(raw_grpc.sensorPortSpec.sensorC)
    else:
        sensor_port_spec['C'] = None

    if len(raw_grpc.sensorPortSpec.sensorD.probeId) > 0:
        sensor_port_spec['D'] = decode_grpc_sensor_port_spec(raw_grpc.sensorPortSpec.sensorD)
    else:
        sensor_port_spec['D'] = None

    return _df, sensor_port_spec


def decode_grpc_sensor_port_spec(grpc_sensor):
    d = {'probe_id': grpc_sensor.probeId,
         'headstage_id': grpc_sensor.headstageId,
         'x_min': grpc_sensor.xMin,
         'x_max': grpc_sensor.xMax,
         'y_min': grpc_sensor.yMin,
         'y_max': grpc_sensor.yMax,
         'wireframe_x': [],
         'wireframe_y': []}
    for pt in grpc_sensor.wireframe.vtx:
        d['wireframe_x'].append(pt.x)
        d['wireframe_y'].append(pt.y)
    return d
