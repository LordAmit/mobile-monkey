'''
telnet to adb connection and management module
'''
import telnetlib
from enum import Enum
import time
import config_reader as config
import util

PRINT_FLAG = True


class NetworkStatus(Enum):

    '''
        Network status possible values
    '''
    gsm = 0
    hscsd = 1
    gprs = 2
    umts = 3
    edge = 4
    hsdpa = 5
    lte = 6
    evdo = 7
    full = 8


class NetworkDelay(Enum):

    '''
    Network delay constants
    '''
    gsm = 0
    edge = 1
    umts = 2
    none = 3


class GsmProfile(Enum):

    '''
    Gsm profile constants
    '''
    STRENGTH0 = 0
    STRENGTH1 = 1
    STRENGTH2 = 2
    STRENGTH3 = 3
    STRENGTH4 = 4


class TelnetAdb:

    '''
    Telnet to Android connector API
    '''
    GSM_BREAK = 10
    telnet = None

    def __init__(self, host: str='localhost',
                 port: int=int(config.EMULATOR_PORT))-> None:
        '''initiates the telnet to adb connection at provided `host`:`port`'''
        self.__establish_connection(host, port)

    def __establish_connection(self, host: str, port: int):
        try:
            self.telnet = telnetlib.Telnet(host, int(port))
        except ConnectionRefusedError:
            raise ConnectionRefusedError("Connection refused")
        self.__telnet_read_until()
        self.__telnet_write_command('auth ' + config.TELNET_KEY)

    def __telnet_write_command(self, command: str):
        util.debug_print(command, flag=PRINT_FLAG)
        telnet_command = bytes("{}\n".format(command), "ascii")
        self.telnet.write(telnet_command)

    def __telnet_read_until(self):
        print(self.telnet.read_until(b'OK'))

    def set_connection_speed(self, speed: NetworkStatus):
        '''
        sets connection speed, where `speed` is `NetworkStatus` type
        '''
        self.__telnet_write_command(
            'network speed ' + str(speed.name))

    def set_connection_delay(self, delay: NetworkDelay):
        '''
        sets connection delay, where `delay` is `NetworkDelay` type
        '''
        self.__telnet_write_command(
            'network delay ' + delay.name)

    def set_gsm_profile(self, profile: GsmProfile):
        '''
        sets GSM profile, where `profile` is `GsmProfile` type.
        takes around 15 seconds for android OS to detect it
        '''
        self.__telnet_write_command('gsm signal-profile ' + str(profile.value))
        time.sleep(self.GSM_BREAK)

    def kill_avd(self):
        '''
        self destructs
        '''
        self.__telnet_write_command('kill')

    def reset_gsm_profile(self):
        '''
        resets GSM profile to signal strength 4
        '''
        self.__telnet_write_command('gsm signal-profile 4')
        time.sleep(self.GSM_BREAK)

    def reset_network_delay(self):
        '''
        resets network delay to 0
        '''
        self.__telnet_write_command('network delay 0')

    def reset_network_speed(self):
        '''
        resets network speed to full
        '''
        self.__telnet_write_command('network speed full')

    def reset_all(self):
        '''
        resets by calling
        >>> self.reset_network_delay()
        >>> self.reset_network_speed()
        >>> self.reset_gsm_profile()
        '''
        print("setting network delay to 0")
        self.reset_network_delay()
        print("setting network speed to full")
        self.reset_network_speed()
        print("resetting GSM profile")
        self.reset_gsm_profile()


if __name__ == '__main__':
    TNC = TelnetAdb(config.LOCALHOST, int(config.EMULATOR_PORT))
    TNC.kill_avd()
