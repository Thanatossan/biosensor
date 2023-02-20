import math
import re
import sched
import sys
import threading
import time

import numpy as np
import pyqtgraph as pg
from agilent_8168D_laser import LaserAgilent8168D
from AQ2140 import Opticalmultimeter
from biosensor_new import Ui_MainWindow
from graph_ui import graph_widget
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout
from splash_screen_ui import Ui_SplashScreen
from PyQt5.QtCore import QThread, QObject, pyqtSignal as Signal, pyqtSlot as Slot
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# import matplotlib.pyplot as plt
class worker(QObject):
    progress = Signal(int)
    

class biosensor_function(Ui_MainWindow,LaserAgilent8168D,Opticalmultimeter):
    # s = sched.scheduler(time.time, time.sleep)

    def __init__(self):
        super().__init__()
        # self.setMouseTracking(True)

        
        # step parameter
        graph_widget(self)
        self.is_connected = False
        self.is_setting_mode = False
        self.is_setting_light_source = False
        self.is_setting_sweep = False
        
        self.is_selected_manual =False


        self.can_continue = False
        # machine parameter
        self.is_laser_on = False
        self.output_value = 1450.0
        self.power_value = -13.80
        self.start_value = 1450.0
        self.delay_value = 1450.0
        self.stop_value = 1450.0
        self.step_value = 0.001
        self.is_W = False  # False if dBm
        self.status = False # True if currently busy
        # result parameter
        # self.measure_plot_list = [[self.x1, self.y1, self.ax1, self.canvas1],
        #                           [self.x2, self.y2, self.ax2, self.canvas2],
        #                           [self.x3, self.y3, self.ax3, self.canvas3],
        #                           [self.x4, self.y4, self.ax4, self.canvas4],
        #                           [self.x5, self.y5, self.ax5, self.canvas5],
        #                           [self.x6, self.y6, self.ax6, self.canvas6],
        #                           [self.x7, self.y7, self.ax7, self.canvas7],
        #                           [self.x8, self.y8, self.ax8, self.canvas8],
        #                           [self.x9, self.y9, self.ax9, self.canvas9],
        #                           [self.x10, self.y10, self.ax10, self.canvas10]]
        # self.resonance_plot_list = [[self.x1r, self.y1r, self.ax1r, self.canvas1r],
        #                             [self.x2r, self.y2r, self.ax2r, self.canvas2r],
        #                             [self.x3r, self.y3r, self.ax3r, self.canvas3r],
        #                             [self.x4r, self.y4r, self.ax4r, self.canvas4r],
        #                             [self.x5r, self.y5r, self.ax5r, self.canvas5r],
        #                             [self.x6r, self.y6r, self.ax6r, self.canvas6r],
        #                             [self.x7r, self.y7r, self.ax7r, self.canvas7r],
        #                             [self.x8r, self.y8r, self.ax8r, self.canvas8r],
        #                             [self.x9r, self.y9r, self.ax9r, self.canvas9r],
        #                             [self.x10r, self.y10r, self.ax10r, self.canvas10r]]

        self.setupUi(MyProgram)
        # page component
        

        ### select style
        self.selected = ("border-style: outset;\n"
            "border-width: 4px;\n"
            "border-radius: 10px;\n"
            "border-color: #000000;\n"
            "color: #FFFFFF;\n"
            "background-color: #9D59BF;\n"
                )
        self.unselected =("background-color: #9D59BF;\n"
                "border-radius: 10px;\n"
                "border:none;\n"
                "color: #FFFFFF;\n"
                    )
        ### step style
        self.not_in_step_button = ("background-color: #BFBFBF;\n"
                "border-radius: 10px;\n"
                "border:none;\n"
                "color: #FFFFFF;\n"
                    )
        self.in_step_button = ("background-color: #9D59BF;\n"
                "border-radius: 10px;\n"
                "border:none;\n"
                "color: #FFFFFF;\n"
                    )
        self.not_in_step_label = ("color:#BFBFBF;")
        self.in_step_label = ("color:#9D59BF;")
        self.in_step_label_unit = ("color:#3AB795;")
        
        self.in_step_input = (
            "color:#9D59BF;\n"
            "border: 2px solid #3AB795;\n"
            "padding: 0 8px;\n"
        )
        # # un-activate
        self.label_settingParameter.setStyleSheet(self.not_in_step_label)
        self.defaultParameter_button.setStyleSheet(self.not_in_step_button)
        self.manualParameter_button.setStyleSheet(self.not_in_step_button)
        self.borderParameter_style = ("#setParameterField{\n"
                                    "border-style: outset;\n"
                                    "border-width: 2px;\n"
                                   "border-radius: 10px;\n"
                                    "border-color: #A49BA8;\n"
                                    "}\n")
        self.setParameterField.setStyleSheet(self.borderParameter_style)
        ## light source field
        self.label_settingLightSource.setStyleSheet(self.not_in_step_label)
        self.label_outputWavelength.setStyleSheet(self.not_in_step_label)
        self.label_outputPower.setStyleSheet(self.not_in_step_label)
        self.input_wavelength.setStyleSheet(self.not_in_step_label)
        self.input_wavelength.setReadOnly(True)
        self.input_power.setStyleSheet(self.not_in_step_label)
        self.input_power.setReadOnly(True)
        self.label_nm_1.setStyleSheet(self.not_in_step_label)
        self.offLaser_button.setStyleSheet(self.not_in_step_button)
        self.onLaser_button.setStyleSheet(self.not_in_step_button)
        self.W_button.setStyleSheet(self.not_in_step_button)
        self.dBm_button.setStyleSheet(self.not_in_step_button)
        self.borderLightSource_style = ("#settingLightSourceField{\n"
                                    "border-style: outset;\n"
                                    "border-width: 2px;\n"
                                   "border-radius: 10px;\n"
                                    "border-color: #A49BA8;\n"
                                    "}\n")
        self.settingLightSourceField.setStyleSheet(self.borderLightSource_style)

        # ## sweep field
        self.label_wavelengthSweep.setStyleSheet(self.not_in_step_label)
        self.label_start.setStyleSheet(self.not_in_step_label)
        self.label_stop.setStyleSheet(self.not_in_step_label)
        self.label_step.setStyleSheet(self.not_in_step_label)
        self.label_stepDelay.setStyleSheet(self.not_in_step_label)
        self.label_stepDelay_2.setStyleSheet(self.not_in_step_label)
        self.label_nm_start.setStyleSheet(self.not_in_step_label)
        self.label_nm_step.setStyleSheet(self.not_in_step_label)
        self.label_nm_stop.setStyleSheet(self.not_in_step_label)
        self.label_ms.setStyleSheet(self.not_in_step_label)
        self.input_start.setReadOnly(True)
        self.input_step.setReadOnly(True)
        self.input_stop.setReadOnly(True)
        self.input_stepdelay.setReadOnly(True)
        self.input_start.setStyleSheet(self.not_in_step_label)
        self.input_step.setStyleSheet(self.not_in_step_label)
        self.input_stop.setStyleSheet(self.not_in_step_label)
        self.input_stepdelay.setStyleSheet(self.not_in_step_label)
        self.borderwavelength_style = ("#wavelenghtSweepField{\n"
                                    "border-style: outset;\n"
                                    "border-width: 2px;\n"
                                   "border-radius: 10px;\n"
                                    "border-color: #A49BA8;\n"
                                    "}\n")
        self.wavelenghtSweepField.setStyleSheet(self.borderwavelength_style)

        # ## progress field
        self.start_button.setStyleSheet(self.not_in_step_button)
        self.stop_button.setStyleSheet(self.not_in_step_button)
        self.label_status.setStyleSheet(self.not_in_step_label)
        self.label_currentStatus.setStyleSheet(self.not_in_step_label)
        self.progressBar.setValue(0)
        # ## connect 
        self.connect_button.clicked.connect(self.connect_instrument);
        # ## Setting param default or manual
        self.defaultParameter_button.clicked.connect(self.default_setting_param);
        self.manualParameter_button.clicked.connect(self.manual_setting_param)

        # ## laser
        
        self.onLaser_button.clicked.connect(self.set_laser_on)
        self.offLaser_button.clicked.connect(self.set_laser_off)

        # # handle input
        self.input_wavelength.textChanged.connect(self.handle_output_wavelength_input)
        self.input_power.textChanged.connect(self.handle_output_power_input)
        self.input_start.textChanged.connect(self.handle_start_input)
        self.input_stop.textChanged.connect(self.handle_stop_input)
        self.input_step.textChanged.connect(self.handle_step_input)
        self.input_stepdelay.textChanged.connect(self.handle_step_delay_input)

        # ## W dBM converter
        self.W_button.clicked.connect(self.dBm_to_W)
        self.dBm_button.clicked.connect(self.W_to_Bm)
        
        # # Start Stop Laser
        self.start_button.clicked.connect(self.sweep_start)
        self.stop_button.clicked.connect(self.sweep_stop)
    
        ## plot graph
        # self.wavelength = [1525,1525.1,1525.2,1525.3,1525.4,1525.5,1525.6,1525.7,1525.8,1525.9,1526,1526.1,1526.2,1526.3,1526.4,1526.5,1526.6,1526.7,1526.8,1526.9,1527,1527.1,1527.2,1527.3,1527.4,1527.5,1527.6,1527.7,1527.8,1527.9,1528,1528.1,1528.2,1528.3,1528.4,1528.5,1528.6,1528.7,1528.8,1528.9,1529,1529.1,1529.2,1529.3,1529.4,1529.5,1529.6,1529.7,1529.8,1529.9,1530,1530.1,1530.2,1530.3,1530.4,1530.5,1530.6,1530.7,1530.8,1530.9,1531,1531.1,1531.2,1531.3,1531.4,1531.5,1531.6,1531.7,1531.8,1531.9,1532,1532.1,1532.2,1532.3,1532.4,1532.5,1532.6,1532.7,1532.8,1532.9,1533,1533.1,1533.2,1533.3,1533.4,1533.5,1533.6,1533.7,1533.8,1533.9,1534,1534.1,1534.2,1534.3,1534.4,1534.5,1534.6,1534.7,1534.8,1534.9,1535,1535.1,1535.2,1535.3,1535.4,1535.5,1535.6,1535.7,1535.8,1535.9,1536,1536.1,1536.2,1536.3,1536.4,1536.5,1536.6,1536.7,1536.8,1536.9,1537,1537.1,1537.2,1537.3,1537.4,1537.5,1537.6,1537.7,1537.8,1537.9,1538,1538.1,1538.2,1538.3,1538.4,1538.5,1538.6,1538.7,1538.8,1538.9,1539,1539.1,1539.2,1539.3,1539.4,1539.5,1539.6,1539.7,1539.8,1539.9,1540]
        # self.power = [-43.7476,-43.7366,-44.1364,-43.1366,-43.0064,-43.9646,-43.4486,-43.5438,-43.5338,-43.6742,-44.586,-43.8858,-43.705,-44.3114,-45.0998,-45.4824,-44.9838,-45.6332,-45.7642,-47.04,-48.3224,-49.8152,-52.2128,-57.3208,-62.7824,-59.2582,-53.8532,-50.0206,-48.6364,-47.192,-46.4956,-46.2394,-45.2796,-45.5998,-45.4058,-45.2596,-45.0862,-45.3528,-45.0098,-45.0648,-44.801,-44.8846,-44.2986,-43.6876,-43.7938,-43.9008,-43.855,-43.7864,-44.9096,-43.977,-43.7568,-43.9912,-44.7348,-43.4874,-43.8444,-44.4074,-43.8796,-44.541,-44.7462,-44.5406,-44.6336,-44.1886,-44.7692,-44.5974,-44.358,-44.1904,-44.3998,-45.3082,-45.9538,-45.4758,-44.783,-46.0478,-45.8224,-45.8488,-46.2736,-47.2618,-47.7482,-50.1782,-50.9202,-53.7232,-59.5948,-65.5182,-58.2672,-52.7968,-50.0944,-48.1658,-47.25,-46.8628,-46.8382,-46.1718,-45.0204,-45.113,-45.7312,-44.9978,-45.4774,-44.5426,-44.6494,-44.809,-44.5738,-44.2668,-44.2128,-43.4992,-44.2868,-44.0858,-43.9556,-43.882,-43.871,-43.8716,-44.313,-44.5612,-44.1392,-43.96,-44.0512,-44.2212,-44.6162,-44.2736,-43.8966,-44.011,-44.8376,-44.1974,-43.895,-44.7772,-44.0686,-44.6928,-44.4762,-44.3902,-45.1422,-44.7348,-45.1646,-46.127,-46.2952,-45.7368,-46.7824,-47.5714,-48.7834,-50.8468,-53.3186,-58.1178,-66.5278,-59.8814,-54.0512,-50.7346,-48.7952,-47.6338,-47.3,-46.0734,-45.2902,-44.8232,-44.9658,-45.0306,-44.7656]
        self.wavelength = []
        self.power = []
        self.dataline=self.fig_result1.plot(self.wavelength, self.power,symbol="o")
        
        

        ## matplot lib
        # self.figure = plt.figure(  dpi=100)
        # self.canvas = FigureCanvas(self.figure)
        # self.toolbar = NavigationToolbar(self.canvas, None)
        # self.graph_field_layout.addWidget(self.toolbar)
        # self.graph_layout.addWidget(self.canvas)
        # self.figure.clear()
        # ax = self.figure.subplots()  
        # ax.plot(self.wavelength,self.power)
        # self.canvas.draw()
    def activate_lightsource(self):
        self.label_settingLightSource.setStyleSheet(self.in_step_label)
        self.label_outputWavelength.setStyleSheet(self.in_step_label)
        self.label_outputPower.setStyleSheet(self.in_step_label)
        self.label_nm_1.setStyleSheet(self.in_step_label_unit)
        self.offLaser_button.setStyleSheet(self.in_step_button)
        self.onLaser_button.setStyleSheet(self.in_step_button)
        self.W_button.setStyleSheet(self.in_step_button)
        self.dBm_button.setStyleSheet(self.in_step_button)
        self.dBm_button.setStyleSheet(self.selected) # get unit before set if dbm skip ; else set dbm unit
        self.borderLightSource_style = ("#settingLightSourceField{\n"
                                    "border-style: outset;\n"
                                    "border-width: 2px;\n"
                                   "border-radius: 10px;\n"
                                    "border-color: #9D59BF;\n"
                                    "}\n")
        self.settingLightSourceField.setStyleSheet(self.borderLightSource_style)
        self.input_wavelength.setStyleSheet(self.in_step_input)
        self.input_power.setStyleSheet(self.in_step_input)
        self.input_wavelength.setReadOnly(False)
        self.input_power.setReadOnly(False)

    def activate_sweep(self):
        self.input_start.setValue(self.start_value)
        self.input_stepdelay.setValue(self.delay_value)
        self.input_stop.setValue(self.stop_value)
        self.input_step.setValue(self.step_value)
        self.label_wavelengthSweep.setStyleSheet(self.in_step_label)
        self.label_start.setStyleSheet(self.in_step_label)
        self.label_stop.setStyleSheet(self.in_step_label)
        self.label_step.setStyleSheet(self.in_step_label)
        self.label_stepDelay.setStyleSheet(self.in_step_label)
        self.label_stepDelay_2.setStyleSheet(self.in_step_label)
        self.label_nm_start.setStyleSheet(self.in_step_label_unit)
        self.label_nm_stop.setStyleSheet(self.in_step_label_unit)
        self.label_ms.setStyleSheet(self.in_step_label_unit)
        self.label_nm_step.setStyleSheet(self.in_step_label_unit)
        self.offLaser_button.setStyleSheet(self.in_step_button)
        self.onLaser_button.setStyleSheet(self.in_step_button)
        self.input_start.setReadOnly(False)
        self.input_stepdelay.setReadOnly(False)
        self.input_stop.setReadOnly(False)
        self.input_step.setReadOnly(False)
        self.input_start.setStyleSheet(self.in_step_input)
        self.input_step.setStyleSheet(self.in_step_input)
        self.input_stop.setStyleSheet(self.in_step_input)
        self.input_stepdelay.setStyleSheet(self.in_step_input)
        self.borderwavelength_style = ("#wavelenghtSweepField{\n"
                                    "border-style: outset;\n"
                                    "border-width: 2px;\n"
                                   "border-radius: 10px;\n"
                                    "border-color: #9D59BF;\n"
                                    "}\n")
        self.wavelenghtSweepField.setStyleSheet(self.borderwavelength_style)
        self.start_button.setStyleSheet(self.in_step_button)
        self.stop_button.setStyleSheet(self.in_step_button)
        self.label_status.setStyleSheet(self.in_step_label)
        self.label_currentStatus.setStyleSheet(self.in_step_label)
        
    def active_plot_result(self):
        pass

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
            self.status_light.setStyleSheet(success)
            self.status_power.setStyleSheet(success)
            # self.can_continue = True
            # self.system_value_set()
            self.status_light.setStyleSheet(success)
            self.status_power.setStyleSheet(success)
            self.is_connected = True
            # setting style to setting parameter field

            self.label_settingParameter.setStyleSheet(self.in_step_label)
            self.defaultParameter_button.setStyleSheet(self.in_step_button)
            self.manualParameter_button.setStyleSheet(self.in_step_button)
            self.borderParameter_style = ("#setParameterField{\n"
                                    "border-style: outset;\n"
                                    "border-width: 2px;\n"
                                   "border-radius: 10px;\n"
                                    "border-color: #9D59BF;\n"
                                    "}\n")
            self.setParameterField.setStyleSheet(self.borderParameter_style)

        except Exception as error:
            print(error)
    ## setting parameter
    def default_setting_param(self):
        self.set_laser_on()
        self.input_wavelength.setValue(self.output_value)
        self.input_power.setValue(self.power_value)
        # try default value
        self.output_value = 1532.0
        self.power_value = 7.0
        self.input_wavelength.setValue(self.output_value)
        self.W_to_Bm()
        self.input_power.setValue(self.power_value)
        
        
        
        self.start_value = 1525.0
        self.delay_value = 2000.0
        self.stop_value = 1540.0
        self.step_value = 0.1
        self.input_start.setValue(self.start_value)
        self.input_stepdelay.setValue(self.delay_value)
        self.input_stop.setValue(self.stop_value)
        self.input_step.setValue(self.step_value)
        self.activate_lightsource()
    def manual_setting_param(self):
        self.set_laser_off()
        # try default value
        self.input_wavelength.setValue(self.output_value)
        self.W_to_Bm()
        self.input_power.setValue(self.power_value)
        self.input_start.setValue(self.start_value)
        self.input_stepdelay.setValue(self.delay_value)
        self.input_stop.setValue(self.stop_value)
        self.input_step.setValue(self.step_value)
        
        self.activate_lightsource()
    ## setting channel
    def setting_channel(self):
        pass
    ###TODO read manual to select channel
    ## laser
    
    def set_laser_on(self):
        try:
            ## Uncomment when test instrusment
            laser_on = threading.Thread(target=self.turn_on())
            laser_on.start()
            laser_on.join()
            
            if self.is_laser_on == False:
                self.offLaser_button.setStyleSheet(self.unselected)
            self.is_laser_on = True
            self.activate_sweep();
            self.onLaser_button.setStyleSheet(self.selected)
            # self.Laser_on.setChecked(True)

        except Exception as error:
            print(error)
    def set_laser_off(self):
        try:
            laser_off = threading.Thread(target=self.turn_off())
            laser_off.start()
            laser_off.join()
            self.offLaser_button.setStyleSheet(self.selected)
            
            if self.is_laser_on == True:
                self.onLaser_button.setStyleSheet(self.unselected)
            self.is_laser_on = False

        except Exception as error:
            print(error)
    def handle_output_wavelength_input(self):
        try:
            self.output_value = self.input_wavelength.value()
            self.set_wavelength_nm(self.output_value)
            print("wavelegnth set")
        except Exception as error:
            print(error)
    def handle_output_power_input(self):
        try:
        
            self.power_value = self.input_power.value()
            self.set_power(self.power_value)
            print("power set")
        except Exception as error:
            print(error )
    def handle_start_input(self):
        try:
            self.start_value = self.input_start.value()
            print(self.start_value)
        except Exception as error:
            print(error)
    def handle_stop_input(self):
        try:
            self.stop_value = self.input_stop.value()
            print(self.stop_value)
        except Exception as error:
            print(error)
    def handle_step_input(self):
        try:
            self.step_value = self.input_step.value()
            print(self.step_value)
        except Exception as error:
            print(error)
    def handle_step_delay_input(self):
        try:
            self.delay_value = self.input_stepdelay.value()
            print(self.delay_value)
        except Exception as error:
            print(error)
    def W_to_Bm(self):
            self.set_unit('dBm')
            if self.is_W:
                if self.is_connected == True:
                    self.is_W = False
                    self.dBm_button.setStyleSheet(self.selected)
                    self.W_button.setStyleSheet(self.unselected)
                    
                    self.set_power(self.power_value)
                    print(self.is_W )
    def dBm_to_W(self):
        self.set_unit('\u00B5mw')
        if self.is_W == False:
            if self.is_connected == True:
                self.dBm_button.setStyleSheet(self.unselected)
                self.W_button.setStyleSheet(self.selected)
                self.is_W = True
                
                self.set_power(self.power_value)
                print(self.is_W )
            
    def laser_busy(self):
        self.label_currentStatus.setText("Busy")
    def laser_idle(self):
        self.label_currentStatus.setText("Idle")
    def laser_start(self):
        self.laser_busy()
    def laser_stop(self):
        self.laser_idle()
        try:
            if ~self.is_laser_on :
                self.set_laser_on()
            self.data.clear()
            self.process_data.clear()
            self.final_data.clear()
            
            # self.measure_plot_list[n][0].clear()
            # self.measure_plot_list[n][1].clear()
        except Exception as error:
            print(error)
    def set_value_function(self):
        try:
            self.set_wavelength_nm(self.output_value)
            if self.is_W :
                self.set_unit(' \u00B5W')
            else:
                self.set_unit(' dBm')
            self.set_power(self.power_value)

        except Exception as error:
            print(error)
    def sweep_start(self):
        # n = self.select_figure.currentIndex()
        n = 0
        try:
            self.set_laser_on()
            self.set_value_function()
            self.data.clear()
            self.process_data.clear()
            self.final_data.clear()
            
            # self.measure_plot_list[n][0].clear()
            # self.measure_plot_list[n][1].clear()
            self.start_button.setDisabled(True)
            self.laser_busy()
            sweep = threading.Thread(target=self.wavelength_sweep, args=(self.start_value,
                                                                         self.stop_value,
                                                                         self.step_value,
                                                                         self.delay_value))
            sweep.start()
            self.update_graph()
            # update_graph_thread = threading.Thread(target=self.update_graph)
            # update_graph_thread.start()

            
        except Exception as error:
            print(error)
    def process_data_function(self):
        try:
            for data in Opticalmultimeter.data:

                a = re.findall("[-+]?\d*\.\d+|\d+", data)
                b = ''.join(a)
                Opticalmultimeter.process_data.append(b)

            Opticalmultimeter.process_data = list(map(float, Opticalmultimeter.process_data))
            Opticalmultimeter.data.clear()
            print('\nprocess data: {}'.format(Opticalmultimeter.process_data))

        except Exception as error:
            print(error)

    def avg_data_for_plot(self):
        avg = sum(Opticalmultimeter.process_data) / len(Opticalmultimeter.process_data)
        # print(type(avg))
        Opticalmultimeter.final_data.append(round(avg,4))
        Opticalmultimeter.process_data.clear()
        print('\navg data: {}'.format(avg))
        print('final data: {}'.format(Opticalmultimeter.final_data))
        return Opticalmultimeter.final_data
    def read_data(self):
        try:
            while len(Opticalmultimeter.data) < 5:
                read_data = self.optical_multimeter.query("OD2")  # channel B
                Opticalmultimeter.data.append(read_data)

        except Exception as error:
            print(error)
    def wavelength_sweep(self,
                         start_wavelength,
                         stop_wavelength,
                         step_wavelength,
                         step_delay
                         ):
        try:
            LaserAgilent8168D.stop_click = False
            for wavelength in np.arange(start_wavelength, stop_wavelength + step_wavelength, step_wavelength):
                if LaserAgilent8168D.stop_click:
                    break
                self.tunable_laser.write(':WAVE {}nm'.format(str(wavelength)))
                if wavelength == start_wavelength:
                    time.sleep(1)
                time.sleep(step_delay / 1000)
                self.read_data()
                self.process_data_function()
                self.power = self.avg_data_for_plot()
                # self.update_plot(wavelength)
                self.wavelength.append(wavelength)
                self.newData.emit(self.wavelength,self.power)
                # print("wavelength"+str(wavelength))
                # self.update_progress2()
            self.laser_idle()
            self.start_button.setEnabled(True)

        except Exception as error:
            print(error)
    def update_graph(self):
        try:
            time.sleep(self.delay_value/1000)
            print("updated graph")
            self.fig_result1.plot(self.wavelength,self.power)
        except Exception as error:
            print(error)
    def sweep_stop(self):
        try:
            LaserAgilent8168D.stop_click = True
            self.laser_idle()
        except Exception as error:
            print(error)
    def update_progress(self, wavelength=None,
                        start_wavelength=None,
                        step_wavelength=None,
                        stop_wavelength=None):

        progress = int(round((wavelength - start_wavelength + step_wavelength) * 100 /
                             (stop_wavelength + step_wavelength - start_wavelength)))
        self.progressBar.setValue(progress)
        
    def update_progress2(self):
        try:
            update = threading.Thread(target=self.update_progress,
                                      args=(self.get_wavelength_nm(), self.start_value, self.step_value,
                                            self.stop_value))
            update.start()

        except Exception as error:
            print(error)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MyProgram = QtWidgets.QMainWindow()
    window = biosensor_function()
    MyProgram.show()
    sys.exit(app.exec_())
