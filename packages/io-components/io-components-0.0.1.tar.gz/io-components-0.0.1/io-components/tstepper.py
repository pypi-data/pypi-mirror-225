#Standard modules
from time import sleep

#Custom modules
from components.logger import logger
from components.component import Component
from components.componentsDrivers.tmcDriver import TMCstepperController
from components.digitalOutput import DigitalOutput
from components.componentsDrivers.TMC5160RegMap import regmap, regmap_mask


class Tstepper(Component):

    cPos = 0
    microStep = 256
    stepsPerTurn = 200
    

    def __init__(self,
                 name,
                 board,        
                 address,
                 speed: int = 100000,
                 accel: int = 14000,
                 homingEndstop = None,
                 homeOffset: float = 0,
                 homingDir: int = 1,
                 homingSpeed: int = None,
                 homingWithdrawDistance: float = 0,
                 ratio: float = 1,
                 maxTravel: float = 999999999999,
                 current: int = 0x01,
                 holdingCurrent: int = 0x05,
                 motorType: str = 'NEMA23',
                 posUnit: str = 'mm',
                 writeCmdCounter: int = 0
                 ):

        """
        :param speed: 0 -> 1 048 575 (*5.619 µsteps/s)
        :param accel: 0 -> 65 535 (*0.2466 µsteps/s²)
        :param homeOffset: distance set as zero position. Motor will move there after homing.
        :param homingDir: value is 1 or 2
        :param homingWithdrawDistance: withdraw distance -for 2nd precise homing- after 1st homing movement. Distance according to ratio.
        :param ratio: distance/turn (ex: 10mm/turn -> ratio = 10)
        :param current: 0 -> 31 (0.147 A -> 4.7 A)
        """ 
        super().__init__(name, board)

        self.name = name
        self.board = board
        self.address = address
        self.maxTravel = maxTravel
        self.speed = speed
        self.accel = accel
        self.homingEndstop = homingEndstop
        self.homeOffset = homeOffset
        self.homingDir = homingDir
        self.homingWithdrawDistance = homingWithdrawDistance
        #modified for the S5
        self.data_enable_pin = DigitalOutput('data_enable_pin', board, 'DE2')
        if homingSpeed == None:
            self.homingSpeed = speed
        else:
            self.homingSpeed = homingSpeed 

        if not self.homingDir in [1, -1]:
            logger.critical(f'[__init__] - Homing dir for {self.name} cannot be \'{homingDir}\'')
            exit()
        elif self.homingDir == 1:
            self.rampHomingConfig = 2
        else:
            self.rampHomingConfig = 1

        self.step = 0
        self.motorType = motorType

        # To calculate the "ratio" parameter, you must ask yourself:
        # How many units (mm or degrees) does my carriage move when my motor does a full turn
        # Example: Motor mounted rigidly to a 12mm pitch leadscrew 
        #          It means then when the motor does a full turn, my carriage moves 12mm
        #          The ratio is then 12/1 => 12

        self.ratio = ratio # gearing ratio of the unit on which the motor is mounted
        self.ratio = self.microStep * self.stepsPerTurn/self.ratio

        self.current = current
        self.holdingCurrent = holdingCurrent

        self.posUnit = posUnit
        self.reg = regmap
        self.regmask= regmap_mask
        
        self.driver = TMCstepperController(board.serial, self.reg, self.address, 1.8, 1, 1, data_enable=self.data_enable_pin)
        self.driver.setAddr(self.address)
        self.tmcInit()
        self.driver.setNAO(1)

    isHomed = False
    pos = 0

    # todo make homing async
    # todo make a security function that prevents a motor from overtravelling

    ###################################################################################

    def tmcInit(self):  # set reasonable typical setting to all motors

        if self.motorType == "NEMA23":
            self.driver.tmcWrite(regmap["CHOPCONF"],[0x00,0x01,0x00,0xC3])
        elif self.motorType == "NEMA34":
            self.driver.tmcWrite(regmap["CHOPCONF"],[0x40,0x01,0x00,0xC3])
        else:
            logger.critical(f"{self.motorType} is not a motor mode for {self.name} stepper motor")

        self.driver.tmcWrite(regmap["IHOLD_IRUN"],[0x00,0x0A,self.current,self.holdingCurrent]) #[0x00,0x01,0x0F,current]
        #self.setCurrent(self.current)
        self.driver.setReg(regmap["XACTUAL"],0)
        self.driver.setReg(regmap["X_ENC"],0)
        self.driver.setReg(regmap["XTARGET"],0)
        self.driver.setReg(regmap["GCONF"],0x04) # 0x0D
        self.driver.setReg(regmap["SW_MODE"],0x00) # 0x1FE
        self.driver.setReg(regmap["RAMPMODE"],0)
        self.driver.setReg(regmap["TPOWER_DOWN"],10)
        self.driver.setReg(regmap["TPWMTHRS"],1000)
    
        self.driver.setReg(regmap["A1"],int(self.accel / 5) )
        self.driver.setReg(regmap["AMAX"],int(self.accel) )
        self.driver.setReg(regmap["DMAX"],int(self.accel) )
        self.driver.setReg(regmap["D1"],int(self.accel / 5))
    
        #self.driver.setReg(regmap["VSTART"],1000)
        self.driver.setReg(regmap["V1"],int(self.speed / 5))
        self.driver.setReg(regmap["VMAX"],self.speed)
        self.driver.setReg(regmap["VSTOP"],10)

    ###################################################################################

    def home(self, force=False, simple=False, needToWithdraw=True):
        
        if self.isHomed and not force:
            logger.warning(f'{self.name} is already homed')
            return True

        else:

            if not simple:
                self.driver.setReg(self.reg["VMAX"], int(self.homingSpeed))
                self.driver.setReg(self.reg["RAMPMODE"], self.rampHomingConfig)
                while not self.homingEndstop.state:
                    pass
            
            if needToWithdraw:
                if self.rampHomingConfig == 1:
                    val = 2
                else:
                    val = 1
                self.setSpeed(self.homingSpeed)
                self.driver.setReg(self.reg["RAMPMODE"], val)
                while self.homingEndstop.state:
                    pass
                if self.homingWithdrawDistance != 0:
                    # self.setSpeed(0)
                    self.moveAndWait(self.homingWithdrawDistance, relative = True)
                else:
                    sleep(0.2)
                    self.setSpeed(0)

                self.setSpeed(self.homingSpeed/5)
            else:
                self.setSpeed(self.homingSpeed)

            
            self.driver.setReg(self.reg["RAMPMODE"], self.rampHomingConfig)
            while not self.homingEndstop.state:
                pass            
            self.setSpeed(0)

            logger.info(f'Travelled {(self.driver.arrayToInt(self.driver.readReg(self.reg["XACTUAL"]))) / self.ratio + self.homeOffset} {self.posUnit} to home')
            self.driver.setReg("XACTUAL", 0)
            self.driver.setReg("RAMPMODE", 0)
            
            if self.homeOffset != 0:
                self.setSpeed(self.speed)
                self.moveAndWait(self.homeOffset) 
                self.setSpeed(0)
                
            self.driver.setReg("XACTUAL", 0)            
            self.driver.setReg("XTARGET", 0)
            self.setSpeed(self.speed)
            self.isHomed=True


        return True

    ###################################################################################
    # Check if the travel is big enough
    
    def checkForTravel(self, pos) -> bool:
        if pos > self.maxTravel:
            logger.critical(f'[checkForTravel] {self.name} was asked to go to {pos}, beyond it\'s max travel of {self.maxTravel}')
            return False
        return True


    ###################################################################################
    # Move to a certain position
    # If target position is negative, do a certain calculation to convert it to byte negative

    def moveToPos(self, pos, relative = False) -> bool:
        if not self.checkForTravel(pos):
            logger.info(f'{self.name} was asked to do a move too long')
            return False
        
        if relative:
            self.driver.setReg(self.reg["XACTUAL"], 0)

        newPos = pos * self.homingDir
        self.steps = round(newPos * self.ratio)
        #print(f'target steps = {self.steps}')

        if newPos > 0: 
            target = self.steps
            self.pos = target
        elif newPos <= 0:
            target = self.steps & 0xffffffff
        
        #self.driver.setReg("RAMPMODE", 0)
        #self.driver.setReg(self.reg["VMAX"], self.speed)
        self.driver.setReg(self.reg["XTARGET"], target)
        #logger.debug(f'[moveToPos] Initiating move from {self.name} to {pos}')
        return True

    ###################################################################################

    def waitForStop(self):
        xActual = self.driver.arrayToInt(self.driver.readReg(self.reg["XACTUAL"]))
        xTarget = self.driver.arrayToInt(self.driver.readReg(self.reg["XTARGET"]))
        
        while (xActual != xTarget):
            sleep(0.05)
            xActual = self.driver.arrayToInt(self.driver.readReg(self.reg["XACTUAL"]))
            #xTarget = self.driver.arrayToInt(self.driver.readReg(self.reg["XTARGET"]))

        return True

    ###################################################################################

    def get_current_pos(self):
        
        xTarget = self.driver.arrayToInt(self.driver.readReg(self.reg["XTARGET"]))
        print(xTarget)
        
    

        return True
    ###################################################################################

    # Enable or disable a motor

    def moveAndWait(self, pos, speed = None, accel = None, relative = False):
        if not speed == None: self.setSpeed(speed)
        if not accel == None: self.setAccel(accel)
        self.moveToPos(pos, relative = relative)        
        self.waitForStop()
        if not speed == None: self.setSpeed(self.speed)
        if not accel == None: self.setAccel(self.accel)

    def moveContinuously(self, dir):
        'dir = 1 means positive direction, dir = -1 means negative direction. Anything else throw an error.'
        if dir*self.homingDir == 1:
            val = 1
        elif dir*self.homingDir == -1:
            val = 2
        else:
            logger.critical(f'[moveContinuously] Dir must be 1 or -1 but is {dir}')
        
        self.driver.setReg(self.reg["VMAX"], self.speed )
        self.driver.setReg(self.reg["RAMPMODE"], val)

    def stopMoving(self):
        self.driver.setReg(self.reg["VMAX"], 0)


    def enableDriver(self, mode):
        if mode:
            pass  # todo check CHOPCONF equivalent for motor enabled
        else:
            self.driver.setReg(self.reg["CHOPCONF"], 0x10410150)
    
    def setSpeed(self, speed):
        self.driver.setReg(self.reg["V1"], int(speed*1.5))
        self.driver.setReg(self.reg["VMAX"], int(speed))

    def setAccel(self, accel):
        self.driver.setReg(regmap["A1"], int(accel*1.5))
        self.driver.setReg(regmap["AMAX"], int(accel))
        self.driver.setReg(regmap["DMAX"], int(accel))
        self.driver.setReg(regmap["D1"], int(accel*1.5))

    def zeroMotorPosition(self):
        self.driver.setReg(regmap["XACTUAL"],0)

    def setCurrent(self, runningCurrent, holdingCurrent=0x19):
        self.driver.tmcWrite(regmap["IHOLD_IRUN"],[0x00,0x0A,runningCurrent, holdingCurrent]) #[0x00,0x01,0x0F,current]
        #self.driver.tmcWrite(regmap["IHOLD_IRUN"],[0b0000, 0x0, current, 0x0, current])