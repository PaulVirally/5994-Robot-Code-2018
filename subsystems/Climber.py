import wpilib
from wpilib.command.subsystem import Subsystem

import RobotMap
import subsystems

class Climber(Subsystem):
    '''
    This is the climber subsystem. This is the thing responsible for climbing the rope.
    '''

    def __init__(self):
        '''Instantiates the Climber object.'''

        super().__init__('Climber')

        self.motor = wpilib.VictorSP(RobotMap.climber.motor)

        self.lastClimbValue = 0

    def climb(self):
        self.motor.set(0.7)
        self.lastClimbValue = 0.7

    def hold(self):
        self.motor.set(0.1)
        self.lastClimbValue = 0.1

    def drop(self):
        self.motor.drop(-0.1)
        self.lastClimbValue = -0.1

    def stop(self):
        self.motor.stop(0)
        self.lastClimbValue = 0

    def getOutput(self):
        return self.lastClimbValue

    def log(self):
        wpilib.SmartDashboard.putNumber('Climber Output', self.getOutput())

    def saveOutput(self):
        return 'climb: {0}\n'.format(self.getOutput())