import pyvisa
rm = pyvisa.ResourceManager()
rm.list_resources()
inst = rm.open_resource('GPIB0::12::INSTR')
print(inst.query("*IDN?"))