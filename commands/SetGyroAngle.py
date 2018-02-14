from wpilib.command import Command
import wpilib
import subsystems

class SetGyroAngle(Command):
    '''
    Sets the gyro to a specified angle by using a "PID" control loop.
    '''

    def __init__(self, target_angle):
        super().__init__('SetGyroAngle')

        self.requires(subsystems.drivetrain)
        self.target_angle = target_angle
        self.shouldEndCount = 0
        self.prevAdjust = 0
        wpilib.SmartDashboard.putBoolean('In PID Mode', False)  


    def initialize(self):
        subsystems.drivetrain.resetGyro()
        subsystems.drivetrain.setSetpoint(self.target_angle)
        wpilib.SmartDashboard.putBoolean('In PID Mode', True)  

    def execute(self):
        error = subsystems.drivetrain.getError()

        propK = 0.35/35

        # Adjustment proportional to the error
        propAdjust = error * propK

        # If the propAdjust is too high, we don't want the robot to
        # get out of control, so force it to be at a lower value
        if abs(propAdjust) > 0.7:
            propAdjust = 0.7 if propAdjust > 0 else -0.7

        # From legacy
        adjust = propAdjust

        # If the adjust is too low, force it to be some minimum
        # value. This ensures that the robot is always moving
        # at least a little bit. This minimum value should be 
        # lowest value that makes the robot move. It should not
        # make the robot move noticeably.
        if abs(adjust < 0.31):
            adjust = 0.31 if adjust > 0 else -0.31

        # I think this was the magic of the algorithm before the
        # accident.
        if abs(self.prevAdjust - adjust) < 0.11:
            adjust += (0.11 if adjust > 0 else -0.11)

        # If we are within our range of error, increment shouldEndCount.
        # This makes sure that we don't just hit our setpoint once while
        # carrying some huge momentum. This forces the robot to slow down
        # to the setpoint. This shouldEndCount will accumulate and the
        # command will only end when this value has hit a certain threshold.
        if abs(subsystems.drivetrain.getError()) <= 1:
            self.shouldEndCount += 1
        else:
            self.shouldEndCount = 0

        # Logging
        wpilib.SmartDashboard.putNumber('PID Adjust', adjust)
        wpilib.SmartDashboard.putNumber('PID Should End Count', self.shouldEndCount)

        # Actually drive with the computed adjust
        subsystems.drivetrain.drive(0, adjust)

        self.prevAdjust = adjust

    def stop(self):
        subsystems.drivetrain.stop()
        wpilib.SmartDashboard.putBoolean('In PID Mode', False)

    def isFinished(self):
        if self.shouldEndCount > 5:
            self.stop()
            return True
        return False