# Standard modules
from time import sleep, time
from components.digitalOutput import DigitalOutput
import threading
# Custom modules
from components.logger import logger
from components.component import Component
from board.board import Board
from functools import wraps

# TODO : Add a timeout mechanism if answer not received for too long


def timing(function):
    """A simple timer decorator"""
    @wraps(function)
    def wrapper(*args, **kwargs):
        start = time()
        result = function(*args, **kwargs)
        end = time()
        print(f"Elapsed time {function.__name__}: {end - start}")
        return result

    return wrapper


class Loadcell(Component):

    name: str
    address: int
    port: int
    timeout: float

    ogTar: float
    tarValue: float
    warningCounter: int
    criticalErrorCounter: int

    def __init__(
        self,
        name,
        board,
        port,
        dataEnablePin,
        timeout=1,
        openOnce=False,
        baudRate=115200,

    ):
        super().__init__(name, board)

        self.name = name
        self.board: Board = board

        self.port = port
        self.baudRate = baudRate
        self.lock = threading.Lock()
        self.dataEnablePin: DigitalOutput = dataEnablePin

        if self.dataEnablePin.pin.type == "EXP":
            self.dataEnablePin.reversed = True

        self.timeout = timeout
        self.portIsOpen = False
        self.openOnce = openOnce

        self.tarValue: float = 0
        self.warningCounter: int = 0
        self.criticalErrorCounter: int = 0

        # self.ogTar: float = self.mass
        # logger.debug(f'[__init__] Boot mass of {self.name} is {self.ogTar}')

    def _write(self, msg):

        self.dataEnablePin.turnOn()
        toSend = msg.encode("utf-8")
        # print(f'Now we are sending {toSend}\r')
        self.board.usbSerial.flushInput()
        self.board.usbSerial.flushOutput()
        self.board.usbSerial.write(toSend + b"\r")

        start = time()
        # end = start + (1/self.baudRate) * 8 * (len(toSend + b'\r') )
        end = start + (1 / self.baudRate) * 10 * (len(toSend) + 1)

        while time() < end:
            pass

        self.dataEnablePin.turnOff()
        # logger.debug(f'[_write] writing {toSend} to {self.name}')

    def _wait(self):
        msg = ""
        sleep(0.0025)

        if self.board.usbSerial.in_waiting > 9:
            msg_pb = self.board.usbSerial.read_all()
            print(f'we have a problem: recevied msg ={msg_pb}')
            self.board.usbSerial.flushInput()
            self.board.usbSerial.flushOutput()
            sleep(0.010)

            return None
        elif self.board.usbSerial.in_waiting < 10 and self.board.usbSerial.in_waiting > 0:
            msg = self.board.usbSerial.read_all()

        unCropped = msg
        cropped = str(msg).replace("\r", "")
        if cropped == unCropped:
            return None
        return msg

    def open_port(self):
        """Open the MAD 56 communication port"""
        self.board.usbSerial.flushInput()
        self.board.usbSerial.flushOutput()

        if self.portIsOpen and self.openOnce:
            return True

        payload = "OP" + str(self.port)

        self._write(payload)
        payload = self._wait()

        if b"OK\r" == payload:
            self.portIsOpen = True
            return True
        else:

            self.warningCounter = self.warningCounter + 1
            self.board.usbSerial.read_all()   # extra read to flush the serial
            self.board.usbSerial.flushInput()
            self.board.usbSerial.flushOutput()
            sleep(0.001)
            # if(payload[1:3] != b'RR'):
            #     self.criticalErrorCounter =self.criticalErrorCounter +1
            #     logger.error('RS485 communication problem')
            #     self.board.usbSerial.flushInput()
            #     self.board.usbSerial.flushOutput()
            return False

    def convert_msg_to_weight(self, payload):
        """convert the msg to numerical value if possible"""
        if payload is None:
            return None
        
        msg_to_str= str(payload)
        # print(f'msg_to_str[0:2] = {msg_to_str[0:3]} msg_to_str[0] = {msg_to_str[(len(msg_to_str)-2) : ]}')
        if msg_to_str[0:3] != """b'N""" or msg_to_str[(len(msg_to_str)-2) : ] != """r'""":
            logger.error(f'Loadcell resp format error with payload = {msg_to_str}')
            return None
        try:
            converted_value = float(payload[1:])
        except ValueError:
            self.warningCounter = self.warningCounter + 1

            self.board.usbSerial.flushInput()
            self.board.usbSerial.flushOutput()
            if payload[1:3] != b"RR":
                self.criticalErrorCounter = self.criticalErrorCounter + 1

            return None
        return converted_value

    def read_mass(self):
        """get loadcell mass"""
        self.board.usbSerial.flushInput()
        self.board.usbSerial.flushOutput()
        payload = None
        weight = None
        count = 0
        while payload is None or weight is None:

            self._write("GN")
            payload = self._wait()

            count += 1
            try:
                logger.debug(f"Payload received by {self.name} is {payload}")
                weight = Loadcell.convert_msg_to_weight(self, payload)

            except ValueError:
                payload = None

            if count > 10:
                logger.critical(
                    f"[read_mass] Coun't read {self.name} mass after {count} tries"
                )
                return False

        if count > 1:
            logger.warning(f"Could read {self.name} mass after {count} tries")

        return weight

    def send_cmd(self, cmd):
        """Send a command to the mad56 """
        payload = None
        self._write(cmd)
        sleep(0.2)
        payload = self._wait()
        print(f"Payload received by {self.name} is {payload}")

    def mesure_weight(self):
        """ messure the weight of a loadcell """
        res = self.open_port()
        while res is False:
            res = self.open_port()
            sleep(0.001)
        mass_reading = self.read_mass()
        while not isinstance(mass_reading, float):
            mass_reading = self.read_mass()
            sleep(0.001)
        return mass_reading

    def mesure_weight_with_correction(self):
        """ messure the weight of a loadcell """
        mass = self.mesure_weight()
        corrected_mass = mass - self.tarValue
        return  corrected_mass

    def tar_scale(self):
        self.tarValue = self.mesure_weight()
        print(f' tarvalue = {self.tarValue}')
        # logger.debug(f'Tar value of {self.name} changed from {formerTarValue} to {self.tarValue}. Original tar is {self.ogTar}.')

    def getWarningCounter(self):
        return self.warningCounter

    @property
    def mass(self) -> float:
        success = False
        errorCounter = 0
        while not success:
            if errorCounter == 10:
                logger.critical(f"Couldn't read loadcell {self.name} data")
                break
            try:
                errorCounter += 1
                mass = self.read_mass() - self.tarValue
                success = True
                logger.debug(
                    f"Mass of {self.name} is {mass} with tarValue at {self.tarValue}"
                )
            except Exception:
                logger.exception(f"Error in loadcell {self.name}")
                pass
        try:
            logger.info(f"Mass on {self.name} is {mass}")
            return mass
        except Exception:
            logger.exception(f"Couldnt read {self.name}")
