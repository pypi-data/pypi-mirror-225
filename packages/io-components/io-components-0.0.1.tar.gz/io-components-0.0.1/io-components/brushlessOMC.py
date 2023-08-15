# Standard modules
from time import time
from serial import Serial
from components.digitalOutput import DigitalOutput
from enum import Enum

# Custom modules
from components.logger import logger
from components.component import Component
from board.board import Board

# Fault State register masks
LOCKED_ROTOR = 0b00000001
OVERCURRENT = 0b00000010
HALL_VAL_ABNORMAL = 0b00000100
BUS_VOLTAGE_2LOW = 0b00001000
BUS_VOLTAGE_2HIGH = 0b00010000
CURRENT_PEAK_ALM = 0b00100000

# MODBUS RTU function parameter
WRITE_CMD = 0x06
READ_CMD = 0x03


class DriverRegisters(Enum):
    GENERAL_CONF: int = 0x00
    MAX_REG_SPEED: int = 0x01
    START_CONF: int = 0x02
    ACCEL_DECEL: int = 0x03
    MAX_CURRENT: int = 0x04
    SPEED: int = 0x05
    BRAKING_FORCE: int = 0x06
    ADDRESS: int = 0x07
    ACTUAL_SPEED: int = 0x18  # read only
    FAULT_STATE: int = 0x1B  # read only


class BrushlessOMC(Component):

    def __init__(self, name, board, address, dataEnablePin, serial, timeout_ms=500, baudRate=9600):
        super().__init__(name, board)

        self.name = name
        self.board: Board = board

        self.address = address
        self.baudRate = baudRate
        self.dataEnablePin: DigitalOutput = dataEnablePin
        self.serial: Serial = serial
        self.timeout_ms = timeout_ms

        if self.dataEnablePin.pin.type == "EXP":
            self.dataEnablePin.reversed = True

    def _MODBUS_CRC16(self, buf: list) -> int:
        table: list[int] = [0x0000, 0xA001]
        crc = 0xFFFF
        i = 0
        bit = 0
        xor = 0
        for i in range(0, len(buf)):
            crc ^= buf[i]
            for bit in range(0, 8):
                xor = crc & 0x01
                crc >>= 1
                crc ^= table[xor]
        return crc

    def _write(self, msg):
        self.dataEnablePin.turnOn()
        print(f'Now we are sending {msg}\r')
        self.serial.flushInput()
        self.serial.flushOutput()
        self.serial.write(msg)
        start = time()
        end = start + (1 / self.baudRate) * 10 * (len(msg) + 1)
        while time() < end:
            pass
        self.dataEnablePin.turnOff()

    def _wait(self) -> bytes:
        msg = ''
        start = time()
        end = start + (self.timeout_ms / 1000)
        while self.serial.in_waiting or msg == '':
            msg = self.serial.readall()
            if(time() > end):
                logger.error("Communication timeout")
        return msg

    # ===== WRITE FUNCTIONS =====

    def enable(self, fwd: bool) -> str:
        toSend = [self.address, WRITE_CMD, 0x80, DriverRegisters.GENERAL_CONF.value]
        if fwd:
            toSend = toSend + [0x09, 0x02]
        else:
            toSend = toSend + [0x0B, 0x02]
        toSend += list(int.to_bytes(self._MODBUS_CRC16(toSend), 2, 'little'))
        self._write(toSend)
        if list(self._wait()) == toSend:
            status = 'OK'
        else:
            status = 'ERROR'
        return status

    def disable(self) -> str:
        toSend = [self.address, WRITE_CMD, 0x80,
                  DriverRegisters.GENERAL_CONF.value]
        toSend = toSend + [0x08, 0x02]
        toSend += list(int.to_bytes(self._MODBUS_CRC16(toSend), 2, 'little'))
        self._write(toSend)
        if list(self._wait()) == toSend:
            status = 'OK'
        else:
            status = 'ERROR'
        return status

    def setSpeed(self, speed: int) -> str:
        if(speed not in range(0, 65535)):
            logger.error("Wrong speed parameter, value shoud be in range [0, 65535]")
            status = 'ERROR'
        else:
            toSend = [self.address, WRITE_CMD, 0x80, DriverRegisters.SPEED.value]
            toSend += list(int.to_bytes(speed, 2, 'little'))
            toSend += list(int.to_bytes(self._MODBUS_CRC16(toSend), 2, 'little'))
            self._write(toSend)
            if list(self._wait()) == toSend:
                status = 'OK'
            else:
                status = 'ERROR'
        return status

    def setMaxRegSpeed(self, maxSpeed: int) -> str:
        if (maxSpeed not in range(0, 65535)):
            logger.error("Wrong maxSpeed parameter, value shoud be in range [0, 65535]")
            status = 'ERROR'
        else:
            toSend = [self.address, WRITE_CMD, 0x80, DriverRegisters.MAX_REG_SPEED.value]
            toSend += list(int.to_bytes(maxSpeed, 2, 'little'))
            toSend += list(int.to_bytes(self._MODBUS_CRC16(toSend), 2, 'little'))
            self._write(toSend)
            if list(self._wait()) == toSend:
                status = 'OK'
            else:
                status = 'ERROR'
        return status

    def setMaxTorque(self, maxTorque: int) -> str:
        if(maxTorque not in range(0, 255)):
            logger.error("Wrong maxTorque parameter, value shoud be in range [0, 255]")
            status = 'ERROR'
        else:
            toSend = [self.address, WRITE_CMD, 0x80, DriverRegisters.START_CONF.value]
            toSend += list(int.to_bytes(maxTorque, 1, 'little'))
            toSend += list(int.to_bytes(0x04, 1, 'little'))
            toSend += list(int.to_bytes(self._MODBUS_CRC16(toSend), 2, 'little'))
            self._write(toSend)
            if list(self._wait()) == toSend:
                status = 'OK'
            else:
                status = 'ERROR'
        return status

    def setAccelDecelTime(self, accel: int, decel: int) -> str:
        if(accel not in range(0, 255)):
            logger.error("Wrong accel parameter, value shoud be in range [0, 255]")
            status = 'ERROR'
        elif(decel not in range(0, 255)):
            logger.error("Wrong decel parameter, value shoud be in range [0, 255]")
            status = 'ERROR'
        else:
            toSend = [self.address, WRITE_CMD, 0x80, DriverRegisters.ACCEL_DECEL.value]
            toSend += list(int.to_bytes(accel, 1, 'little'))
            toSend += list(int.to_bytes(decel, 1, 'little'))
            toSend += list(int.to_bytes(self._MODBUS_CRC16(toSend), 2, 'little'))
            self._write(toSend)
            if list(self._wait()) == toSend:
                status = 'OK'
            else:
                status = 'ERROR'
        return status

    def setMaxCurrent(self, maxCurrent: float) -> str:
        if(maxCurrent < 0.0 or maxCurrent > 13.0):
            logger.error("Wrong maxCurrent parameter, value shoud be in range [0.0A, 13.0A]")
            status = 'ERROR'
        else:
            current = (int)(maxCurrent * 144 / 13)
            toSend = [self.address, WRITE_CMD, 0x80, DriverRegisters.MAX_CURRENT.value]
            toSend += list(int.to_bytes(current, 1, 'little'))
            toSend += list(int.to_bytes(0x0F, 1, 'little'))
            toSend += list(int.to_bytes(self._MODBUS_CRC16(toSend), 2, 'little'))
            self._write(toSend)
            if list(self._wait()) == toSend:
                status = 'OK'
            else:
                status = 'ERROR'
        return status

    def setAddress(self, addr: int) -> str:
        if(addr not in range(1, 250)):
            logger.error("Wrong addr parameter, value shoud be in range [1, 250]")
            status = 'ERROR'
        else:
            toSend = [self.address, WRITE_CMD, 0x80, DriverRegisters.ADDRESS.value]
            toSend += list(int.to_bytes(addr, 1, 'little'))
            toSend += list(int.to_bytes(0x00, 1, 'little'))
            toSend += list(int.to_bytes(self._MODBUS_CRC16(toSend), 2, 'little'))
            self._write(toSend)
            if list(self._wait()) == toSend:
                status = 'OK'
                self.address= addr
            else:
                status = 'ERROR'
        return status

    # ===== READ FUNCTIONS =====

    def getSpeed(self) -> int:
        toSend = [self.address, READ_CMD, 0x80, DriverRegisters.ACTUAL_SPEED.value]
        toSend += [0x00, 0x01]
        toSend += list(int.to_bytes(self._MODBUS_CRC16(toSend), 2, 'little'))
        self._write(toSend)
        reply = list(self._wait())
        print(f'motor reply = {reply}')
        actualSpeed = reply[3] | reply[4] << 8
        return (int)(actualSpeed * 16 / 3)

    def readFaultState(self) -> str:
        toSend = [self.address, READ_CMD, 0x80, DriverRegisters.FAULT_STATE.value]
        toSend += [0x00, 0x01]
        toSend += list(int.to_bytes(self._MODBUS_CRC16(toSend), 2, 'little'))
        self._write(toSend)
        reply = list(self._wait())
        print(reply)
        if(reply[3] & LOCKED_ROTOR):
            faultState = 'LOCKED_ROTOR'
        elif(reply[3] & OVERCURRENT):
            faultState = 'OVERCURRENT'
        elif(reply[3] & HALL_VAL_ABNORMAL):
            faultState = 'HALL_VALUE_ABNORMAL'
        elif(reply[3] & BUS_VOLTAGE_2LOW):
            faultState = 'BUS_VOLTAGE_TOO_LOW'
        elif(reply[3] & BUS_VOLTAGE_2HIGH):
            faultState = 'BUS_VOLTAGE_TOO_HIGH'
        elif(reply[3] & CURRENT_PEAK_ALM):
            faultState = 'CURRENT_PEAK_ALARM'
        else:
            faultState = 'OK'
        return faultState
