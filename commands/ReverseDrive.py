from wpilib.command import Command

import OI
import subsystems
import Utils

class ReverseDrive(Command):
    '''
    Drives the robot backwards along what the joystick says, but smooths out
    the input from the joystick
    '''

    def __init__(self):
        super().__init__('Reverse Drive')

        self.requires(subsystems.drivetrain)

    def execute(self):
        # Get the values from the joystick
        joySpeed = oi.getJoySpeed()
        joyTurn = oi.getJoyTurn()

        # Put the values through the sigmoid function
        # to smooth them out
        smoothing = 4 # TODO: Put this on the smart dashboard??
        sigJoySpeed = 2*utils.sigmoid(joySpeed, a=smoothing)-1
        sigJoyTurn = 2*utils.sigmoid(joyTurn, a=smoothing)-1
        s1   = 2*utils.sigmoid(1, a=smoothing)-1
        sn1  = 2*utils.sigmoid(-1, a=smoothing)-1

        # Make sure out speed goes from -1 to 1
        speed = utils.remap(sigJoySpeed, sn1, s1, -1, 1)
        turn = utils.remap(sigJoyTurn, sn1, s1, -1, 1)

        # Drive backwards
        subsystems.drivetrain.drive(-speed, -turn)

    def stop(self):
        subsystems.drivetrain.stop()