# Standard library modules
from components.logger import logger
# Custom modules
from components.component import Component


class DigitalInput(Component):

    name: str
    state: bool = False

    def __init__(self, name, board, pin, reversedState: bool = False):
        super().__init__(name, board)
        self.name = name  # name of the valve for retrival and logging purposes
        if isinstance(pin, str):
            self.pin = board.find(pin)
        else:
            self.pin = pin
        self.pin.modeSetup('INPUT')
        self.reversedState = reversedState

    @property
    def state(self) -> bool:
        value = self.pin.read()
        if self.reversedState == True:
            value = not value
        logger.debug(f'[state] {self.name} is in state {value}')
        return value
