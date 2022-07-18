import pyvisa

class Opticalmultimeter(object):
    data = []
    process_data = []
    final_data = []

    def __init__(self, GPIB2='GPIB0::19::INSTR'):
        GPIB2 = 'GPIB0::19::INSTR'

    def close(self):
        self.optical_multimeter.close()

    def startup_optical_multimeter(self, GPIB):
        rm = pyvisa.ResourceManager()
        self.optical_multimeter = rm.open_resource(GPIB)
        self.optical_multimeter.timeout = 5000

    def zero_set(self):
        self.optical_multimeter.write('Z')

    def set_optical_mod_mode(self, mode):
        ''' CW, 270Hz, 1 kHz, 2 kHz '''
        assert mode.upper() in ('MO0', 'C', 'MO1', 'P', 'MO2', 'MO3')
        self.optical_multimeter.write(str(mode))

    def clear_maxmin_measurement(self):
        self.optical_multimeter.write('H0')

    def start_maxmin_measurement(self):
        self.optical_multimeter.write('H1')

    def channel_setup(self, channel):
        '''
        A and B : C0 or C3
        A       : C1
        B       : C2
        '''
        assert channel.lower() in ('c0', 'c3', 'c1', 'c2')
        self.optical_multimeter.write(channel)

    def measurement_unit(self, unit):
        '''
            W   : FA
            dBm : FB
        '''
        assert str(unit).lower() in ('fa', 'fb')
        self.optical_multimeter.write(unit)

    def range_setup(self, _range):
        range = {
            'AUTO'            : 'RA',
            '30 dBm'          : 'RC',
            '20 dBm'          : 'RD',
            '10 dBm'          : 'RE',
            '0 dBm'           : 'RF',
            '-10 dBm'         : 'RG',
            '-20 dBm'         : 'RH',
            '-30 dBm'         : 'RI',
            '-40 dBm'         : 'RJ',
            'Hold the present': 'RO',
            'range'           : 'RZ',
        }
        self.optical_multimeter.write(range.get(_range))

    def averaging(self, _avg):
        avg = {
            1  : 'AA',
            2  : 'AB',
            5  : 'AC',
            10 : 'AD',
            20 : 'AE',
            50 : 'AF',
            100: 'AG',
            200: 'AH',
        }
        self.optical_multimeter.write(avg.get(_avg))

    def display_resolution(self, _resolution):
        resolution = {
            '1/1000': 'B0',
            '1/100' : 'B1',
            '1/10'  : 'B2',
        }
        self.optical_multimeter.write(resolution.get(_resolution))

    def measurement_interval(self, _time_ms):
        time_ms = {
            10 : 'TA7',
            20 : 'TA8',
            50 : 'TA9',
            100: 'TAA',
            200: 'TAB',
        }
        self.optical_multimeter.write(time_ms.get(_time_ms))

    def measurement(self, m):
        '''
            S : Single time measurement
            F : Continuous measurement
        '''
        assert str(m).lower() in ('s', 'f')
        self.optical_multimeter.write(m)

    def optical_output(self, output):
        '''
            O0 : OFF
            O1 : ON
        '''
        assert str(output).lower() in ('o0', 'o1')
        self.optical_multimeter.write(output)

    def data_storage_title(self, x, title):
        '''
        x     : 1 = A
                2 = B
        title : name of storaging
        '''
        self.optical_multimeter.write('OM{}/TITLE/{}'.format(x, title))

    def set_storage_time(self, ss=None, mm=None, hh=None):
        '''
        Set storage time.
            hh: Hours(0-99)
            
        :param ss:
        :param mm:
        :param hh:
        :return:
        '''
        self.optical_multimeter.write('OM/TIME/{}{}{}'.format(hh, mm, ss))