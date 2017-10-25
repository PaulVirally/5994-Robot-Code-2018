from wpilib.command import Command

import subsystems

class Record(Command):
    '''
    Play back a recording from a specified file to the subsystems
    '''

    def __init__(self, filePath):
        super().__init__('Record')
        
        subsystems.readRecording(filePath)

    def execute(self):
        subsystems.playRecording()

    def stop(self):
        subsystems.stop()