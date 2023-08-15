from components.component import Component
from board.pin import Pin
from board.board import Board
from components.logger import logger


class DigitalOutput(Component):

    name: str
    state: bool = False

    def __init__(self, name, board: Board, pin, reversed_logic=False):
        super().__init__(name, board)
        self.name = name  # Name of the component for logging purposes
        self.pin: Pin = board.find(pin)
        self.pin.modeSetup('OUTPUT')
        self.pin.write(False)
        self.reversed = reversed_logic

    def turnOn(self):
        self.pin.write(True ^ self.reversed)
        self.state = True ^ self.reversed
        logger.debug(f'[turnOn] Turning ON {self.name}')
        # print(f'[turnOn] Turning ON {self.name}')

    def turnOff(self):
        self.pin.write(False ^ self.reversed)
        self.state = False ^ self.reversed
        logger.debug(f'[turnOff] Turning OFF {self.name}')
        # print(f'[turnOff] Turning OFF {self.name}')

    def toggle(self):
        if self.state:
            self.turnOff()
        else:
            self.turnOn()
