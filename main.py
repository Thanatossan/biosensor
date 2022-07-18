from PyQt5 import QtWidgets
from biosensor import Ui_MainWindow
import sys
import time
from AQ2140 import Opticalmultimeter
from agilent_8168D_laser import LaserAgilent8168D
import threading
import sched, time

class biosensor_function(Ui_MainWindow,LaserAgilent8168D,Opticalmultimeter):
    s = sched.scheduler(time.time, time.sleep)
    
    def __init__(self):
        super().__init__()
        self.can_continue = False
        self.is_laser_on = False
        self.output_value = 0.0
        self.frequency_value = 0.0
        self.power_value = 0.0
        self.start_value = 0.0
        self.delay_value = 0.0
        self.stop_value = 0.0
        self.step_value =0.0
        self.setupUi(MyProgram)
        self.basicmode_button.clicked.connect(self.go_connectpage)
        self.advancemode_button.clicked.connect(self.go_advance_page)
        self.connect_button.clicked.connect(self.connect_instrument)
        self.back_button_5.clicked.connect(self.go_mainpage)
        self.back_button_6.clicked.connect(self.go_connectpage)
        self.next_button_3.clicked.connect(self.connect_continue)
        self.manualParameter_button.clicked.connect(self.set_mannaul_parameter)
        self.onLaser_button.clicked.connect(self.set_laser_on)
        self.offLaser_button.clicked.connect(self.set_laser_off)
        self.next_button.clicked.connect(self.go_lightsourcePage)
        self.back_button.clicked.connect(self.go_manaul_or_defualt_page)
        self.back_button_2.clicked.connect(self.set_mannaul_parameter)
        self.next_button_2.clicked.connect(self.go_overall_page)
        self.defaultParameter_button.clicked.connect(self.set_default_parameter)
        self.back_button_4.clicked.connect(self.go_lightsourcePage)
        self.stackedWidget.setCurrentIndex(0)
        self.wavelength_value = 0
        self.frequency_value = 0.0
        self.power_value = 0.0
        self.start_value = 0.0
        self.delay_value = 0.0
        self.stop_value = 0.0
        self.step_value =0.0
        self.input_wavelength.valueChanged.connect(self.set_input_wavelength)
        self.input_freq.valueChanged.connect(self.set_input_freq)
        self.input_pow.valueChanged.connect(self.set_input_power)
        self.input_start.valueChanged.connect(self.set_input_start)
        self.delay_input.valueChanged.connect(self.set_delay_input)
        self.stop_input.valueChanged.connect(self.set_stop_input)
        self.step_input.valueChanged.connect(self.set_step_input)
        self.channel = 0 # 0 is A 1 is B
        self.radioButton_channelA.toggled.connect(self.set_channelA)
        self.radioButton_channelB.toggled.connect(self.set_channelB)
    def set_channelA(self):
        self.channel = 0;
    def set_channelB(self):
        self.channel = 1;
    def set_input_wavelength(self):
        self.wavelength_value = self.input_wavelength.value()
        self.wavelength_value_label.setText(str(self.wavelength_value))
    def set_input_freq(self):
        self.frequency_value = self.input_freq.value()
        self.frequency_value_label.setText(str(self.frequency_value))
    def set_input_power(self):
        self.power_value = self.input_pow.value()
        self.power_value_label.setText(str(self.power_value))
    def set_input_start(self):
        self.start_value = self.input_start.value()
        self.start_value_label.setText(str(self.start_value))
    def set_delay_input(self):
        self.delay_value = self.delay_input.value()
        self.delay_value_label.setText(str(self.delay_value))
    def set_stop_input(self):
        self.stop_value = self.stop_input.value()
        self.stop_value_label.setText(str(self.stop_value))
    def set_step_input(self):
        self.step_value = self.step_input.value()
        self.step_value_label.setText(str(self.step_value))
    
    def go_mainpage(self):
        self.stackedWidget.setCurrentIndex(0)
    def go_connectpage(self):
        self.stackedWidget.setCurrentIndex(1)
    def go_manaul_or_defualt_page(self):
        self.stackedWidget.setCurrentIndex(2)
    def connect_continue(self):
        if self.can_continue == True:
            self.go_manaul_or_defualt_page()
    def set_default_parameter(self):
        #TODO set defualt parameter to all field
        self.stackedWidget.setCurrentIndex(5)
    def set_mannaul_parameter(self):
        self.stackedWidget.setCurrentIndex(3)
        self.defaultParameter_button_2.setStyleSheet(
            "background-color: #9D59BF;\n"
            "border-style: outset;\n"
            "border-width: 4px;\n"
            "border-radius: 10px;\n"
            "border-color: #000000;\n"
            "color: #FFFFFF;\n"
        )
    def go_lightsourcePage(self):
        self.stackedWidget.setCurrentIndex(4)
    def go_overall_page(self):
        self.stackedWidget.setCurrentIndex(5)
    def go_advance_page(self):
        self.stackedWidget.setCurrentIndex(8)
        self.manualParameter_button_2.setStyleSheet(
            "background-color: #9D59BF;\n"
            "border-style: outset;\n"
            "border-width: 4px;\n"
            "border-radius: 10px;\n"
            "border-color: #000000;\n"
            "color: #FFFFFF;\n"
        )
    def connect_instrument(self):
        success = ("background-color: #3AB795;\n"
                   "border-radius: 10px;\n"
                   "border-style: outset;")
        failure = ("background-color: #ff6961;\n"
                   "border-radius: 10px;\n"
                   "border-style: outset;")
        try:
            self.startup_tunable_laser(GPIB='GPIB0::15::INSTR')
            self.startup_optical_multimeter(GPIB='GPIB0::19::INSTR')
            print(self.tunable_laser.query("IDN?"))
            # if self.tunable_laser.query("IDN?") ==  1:
            self.status_lightSource.setStyleSheet(success)
            self.status_powerMeter.setStyleSheet(success)
            self.can_continue = True
            self.next_button_3.setStyleSheet(("background-color: #9D59BF;\n"
                "border-radius: 10px;\n"
                "border:none;\n"
                "color: #FFFFFF;"
                ))
            self.system_value_set()
            self.status_lightSource.setStyleSheet(success)
            self.status_powerMeter.setStyleSheet(success)
            self.can_continue = True
            self.next_button_3.setStyleSheet(("background-color: #9D59BF;\n"
                "border-radius: 10px;\n"
                "border:none;\n"
                "color: #FFFFFF;"
                ))
            # self.system_value_set()
        except Exception as error:
            print(error)
    def system_value_set(self):
        try:
            self.Output_wave.setMinimum(self.wave_range()[0])
            self.Output_wave.setMaximum(self.wave_range()[1])
            self.Wave_hSlider.setMinimum(self.wave_range()[0])
            self.Wave_hSlider.setMaximum(self.wave_range()[1])
            self.Output_wave.setValue(self.get_wavelength_nm())

            self.Output_pow.setMinimum(self.power_range()[0])
            self.Output_pow.setMaximum(self.power_range()[1])
            self.Power_hSlider.setMinimum(self.power_range()[0])
            self.Power_hSlider.setMaximum(self.power_range()[1])
            self.Output_pow.setValue(self.get_power())

            self.start_wave.setMinimum(self.min_wave)
            self.start_wave.setMaximum(self.max_wave)
            self.start_wave_slider.setMinimum(self.min_wave)
            self.start_wave_slider.setMaximum(self.max_wave)
            self.stop_wave.setMinimum(self.min_wave)
            self.stop_wave.setMaximum(self.max_wave)
            self.stop_wave_slider.setMinimum(self.min_wave)
            self.stop_wave_slider.setMaximum(self.max_wave)

        except Exception as error:
            print(error)
    
    
    def set_power_meter(self):
        pass
    def set_laser_on(self):
        try:
            ## Uncomment when test instrusment
            # laser_on = threading.Thread(target=self.turn_on())
            # laser_on.start()
            # laser_on.join()
            self.onLaser_button.setStyleSheet(("border-style: outset;\n"
            "border-width: 4px;\n"
            "border-radius: 10px;\n"
            "border-color: #000000;\n"
            "color: #FFFFFF;\n"
            "background-color: #9D59BF;\n"
                ))
            self.onLaser_button_2.setStyleSheet(("border-style: outset;\n"
            "border-width: 4px;\n"
            "border-radius: 10px;\n"
            "border-color: #000000;\n"
            "color: #FFFFFF;\n"
            "background-color: #9D59BF;\n"
                ))
            if self.is_laser_on == False:
                self.offLaser_button.setStyleSheet(("background-color: #9D59BF;\n"
                "border-radius: 10px;\n"
                "border:none;\n"
                "color: #FFFFFF;\n"
                    ))
                self.offLaser_button_2.setStyleSheet(("background-color: #9D59BF;\n"
                "border-radius: 10px;\n"
                "border:none;\n"
                "color: #FFFFFF;\n"
                    ))
            self.is_laser_on = True
            # self.Laser_on.setChecked(True)

        except Exception as error:
            print(error)

    def set_laser_off(self):
        try:
            # laser_off = threading.Thread(target=self.turn_off())
            # laser_off.start()
            # laser_off.join()
            # self.Laser_off.setChecked(True)
            self.offLaser_button.setStyleSheet(("border-style: outset;\n"
            "border-width: 4px;\n"
            "border-radius: 10px;\n"
            "border-color: #000000;\n"
            "color: #FFFFFF;\n"
            "background-color: #9D59BF;\n"
                ))
            self.offLaser_button_2.setStyleSheet(("border-style: outset;\n"
            "border-width: 4px;\n"
            "border-radius: 10px;\n"
            "border-color: #000000;\n"
            "color: #FFFFFF;\n"
            "background-color: #9D59BF;\n"
                ))
            if self.is_laser_on == True:
                self.onLaser_button.setStyleSheet(("background-color: #9D59BF;\n"
                "border-radius: 10px;\n"
                "border:none;\n"
                "color: #FFFFFF;\n"
                    ))
                self.onLaser_button_2.setStyleSheet(("background-color: #9D59BF;\n"
                "border-radius: 10px;\n"
                "border:none;\n"
                "color: #FFFFFF;\n"
                    ))
            self.is_laser_on = False

        except Exception as error:
            print(error)
    
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MyProgram = QtWidgets.QMainWindow()
    window = biosensor_function()
    MyProgram.show()
    sys.exit(app.exec_())
