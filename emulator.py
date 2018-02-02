'''
nothing here really.
'''


class Emulator:
    '''
    Emulator class. Holds information about port, PID and model of running emulators
    '''

    def __init__(self, emulator_port: int, emulator_pid: int,
                 emulator_model: str)-> None:
        self.port = emulator_port
        self.pid = emulator_pid
        self.model = emulator_model

    def __str__(self):
        return "Port: " + str(self.port) + "\n" + "PID: " + \
            str(self.pid) + "\n" + "Model: " + self.model + "\n"
