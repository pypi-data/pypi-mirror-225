# Standard modules

# Custom modules
from components.digitalOutput import DigitalOutput
from components.logger import logger
from components.component import Component
from components.componentsDrivers.MAX31865_module import MAX31865
from time import time


class Pt100(Component):

    def __init__(self, name, board, cs, wires=4, rtd_nominal=100.0, ref_resistor=402):  # 122.1
        self.name = name
        self.cs: DigitalOutput = cs

        if self.cs.pin.type == "EXP":
            self.cs.reversed = True

        self.cs.turnOn()
        super().__init__(name, board)
        self.device = MAX31865(
            board, cs, wires=wires, rtd_nominal=rtd_nominal, ref_resistor=ref_resistor)

    @property
    def temp(self):
        self.cs.turnOff()
        temps = []
        numberOfSample = 1
        for i in range(numberOfSample):
            temps.append(self.device.temperature)

        temperature = sum(temps) / numberOfSample
        self.cs.turnOn()
        logger.debug(f'Temperature of {self.name} is {temperature}')
        return temperature
