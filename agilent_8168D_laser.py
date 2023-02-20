import math
import pyvisa
from AQ2140 import Opticalmultimeter

class LaserAgilent8168D(Opticalmultimeter):
    stop_click = False

    def __init__(self, GPIB='GPIB0::15::INSTR'):
        super().__init__()

    def startup_tunable_laser(self, GPIB='GPIB0::15::INSTR'):
        rm = pyvisa.ResourceManager()
        self.tunable_laser = rm.open_resource(GPIB)
        self.tunable_laser.timeout = 5000
        print(self.tunable_laser.query('*IDN?'))
        return self.tunable_laser.query('*IDN?')
    def wave_range(self):
        try:
            min_wave = self.tunable_laser.query(':wave? min')
            max_wave = self.tunable_laser.query(':wave? max')
            self.min_wave = float(min_wave) / 1e-9
            self.max_wave = float(max_wave) / 1e-9
            return self.min_wave, self.max_wave

        except Exception as error:
            print(error)

    def power_range(self):
        try:
            min_power = self.tunable_laser.query(':pow? min')
            max_power = self.tunable_laser.query(':pow? max')
            if self.get_unit() == 'dBm':
                self.min_power = float(min_power)
                self.max_power = float(max_power)

            elif self.get_unit() == 'W':
                self.min_power = float(min_power) / 1e-6
                self.max_power = float(max_power) / 1e-6
            return self.min_power, self.max_power

        except Exception as error:
            print(error)

    def laser_close(self):
        self.tunable_laser.close()

    def clear_all(self):
        ''' Reset Command and Clear Status Command '''
        self.tunable_laser.write('*RST;*CLS')

    def turn_on(self):
        # Turn laser on.
        self.tunable_laser.write('output 1')

    def turn_off(self):
        # Turn laser off.
        self.tunable_laser.write('output 0')

    def get_on_or_off(self):
        on_off = self.tunable_laser.query('output?')
        return bool(int(on_off))

    def set_unit(self, unit):
        assert unit.lower().strip() in ('dbm', '\u00B5mw', 'mw')
        if unit.lower().strip() == '\u00B5mw':
            unit = 'mw'
            print("mW")
        elif unit.lower().strip() == 'dbm':
            unit = 'dbm'
        cmd = ':power:unit %s' % unit
        self.tunable_laser.write(cmd)
        self._power_unit = self.get_unit()
        
        return self._power_unit

    def get_unit(self):
        unit = ':power:unit?'
        data = self.tunable_laser.query(unit)
        unit = int(data)
        if unit == 0:
            unit_str = 'dBm'
        else:
            unit_str = 'mW'
            
        return unit_str

    def set_power(self, power):
        if self._power_unit == 'dBm':
            cmd = ':power %fdbm' % power

        elif self._power_unit == 'mW':
            cmd = ':pow %fmw' % power
        self.tunable_laser.write(cmd)

        return self.get_power()

    def get_power(self):
        power = ':pow?'
        data = self.tunable_laser.query(power)
        if self.get_unit() == 'dBm':
            return float(data)
        else:
            return float(data) / 1e-6

    def set_wavelength_nm(self, wavelength_nm):
        cmd = ':wavelength %fnm' % wavelength_nm
        self.tunable_laser.write(cmd)
        r = self.get_wavelength_nm()
        return r

    def get_wavelength_nm(self):
        cmd = ':wavelength?'
        r = self.tunable_laser.query(cmd)
        return float(r) / 1e-9

    def last_operation_completed(self):
        return self.tunable_laser.query('*OPC?')

    def wait_for_last_operation_completed(self):
        finish = False
        while not finish:
            finish = self.last_operation_completed()
        return finish

    def set_modulation_type(self, type):
        ''''
            0 : internal modulation
            1 : coherence control
            2 : external modulation
        '''
        m = type.lower()
        assert m in ('int', '0', 'int2', '1', 'ext', '2')
        self.tunable_laser.write(':AM:SOUR %s' % m)
        return self.get_modulation_type()

    def get_modulation_type(self):
        return self.tunable_laser.query(':AM:SOUR?')

    def set_modulation_output(self, modout):
        '''
            0 or FRQ : modulation signal is output all the time
            1 or FRQDRY : modulation signal is combined with the laser-ready signal
        '''
        assert modout.lower() in ('frq', '0', 'frqdry', '1')
        cmd = ':MODOUT %s' % modout
        self.tunable_laser.write(cmd)
        r = self.get_modulation_output()
        return r

    def get_modulation_output(self):
        return self.tunable_laser.query(':MODOUT?')

    def Save(self, location):
        '''1,2,3,4,5'''
        assert location in ('1', '2', '3', '4', '5')
        self.tunable_laser.write('*sav ' + str(location))  # save การตั้งค่า(1-5)

    def Recall(self, location):
        ''' recall instrument setting '''
        assert location in ('0', '1', '2', '3', '4', '5')
        self.tunable_laser.write('*rcl ' + str(location))

    def set_AM_frequency(self, AM_frequency):
        cmd = ':AM:INTernal:FREQuency %f' % AM_frequency
        self.tunable_laser.write(cmd)
        r = self.get_AM_frequency()
        return r

    def get_AM_frequency(self):
        return self.tunable_laser.query(':AM:INTernal:FREQuency?')

    def dbm_to_microwatts(self,power_dbm):
        power_W = 10. ** (power_dbm / 10.) / 1.e-3
        return power_W

    def microwatts_to_dbm(self,power_W):
        power_dbm = 10. * math.log10(power_W / 1.e+3)
        return power_dbm

if __name__ == '__main__':
    pass
