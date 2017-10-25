import wpilib
from wpilib.command.subsystem import Subsystem

from commands.SmoothFollowJoystick import SmoothFollowJoystick
import RobotMap
import subsystems

class Drivetrain(Subsystem):
    '''
    This is the drivetrain subsystem
    '''

    def __init__(self):
        '''Instantiates the drivetrain object.'''

        super().__init__('Drivetrain')

        self.drivetrain = wpilib.RobotDrive(RobotMap.drivetrain.frontLeftMotor, RobotMap.drivetrain.rearLeftMotor,
                                            RobotMap.drivetrain.frontRightMotor, RobotMap.drivetrain.rearRightMotor)

        self.lastMoveValue = 0
        self.lastRotateValue = 0

    def drive(self, moveValue, rotateValue):
        '''Arcade drive'''
        self.drivetrain.arcadeDrive(moveValue, rotateValue)
        self.lastMoveValue = moveValue
        self.lastRotateValue = rotateValue

    def stop(self):
        self.drive(0, 0)

    def initDefaultCommand(self):
        self.setDefaultCommand(SmoothFollowJoystick())

    def getSpeed(self):
        return self.lastMoveValue

    def getRotate(self):
        return self.lastRotateValue

    def log(self):
        wpilib.SmartDashboard.putNumber('Speed Output', self.getSpeed())
        wpilib.SmartDashboard.putNumber('Rotate Output', self.getRotate())

    def saveOutput(self):
        return 'move: {0}\rotate: {1}\n'.format(self.getSpeed(), self.getRotate())

    def playFromRecording(self, recording):
        '''
        This plays back a certain recording, but only using
        the values that are useful for the drivetrain
        '''

        lines = recording.split('\n')

        for l in lines:
            if l.startswith('move'):
                moveValue = float(l.rstrip()[len('move: '):])
            elif l.startswith('turn'):
                turnValue = float(l.rstrip()[len('turn: '):])

        self.drive(moveValue, turnValue)