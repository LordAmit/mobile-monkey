import subprocess
from enum import Enum, auto

import config_reader as config
import api_commands
import util

ADB = config.adb
PRINT_FLAG = False


class KeyEvent(Enum):

    '''
    Keyboard events
    '''
    # KEYCODE_UNKNOWN = ()
    # KEYCODE_SOFT_RIGHT = ()
    # KEYCODE_HOME = ()
    # KEYCODE_BACK = ()
    # KEYCODE_CALL = ()
    # KEYCODE_ENDCALL = auto()
    KEYCODE_0 = 0
    KEYCODE_1 = auto()
    KEYCODE_2 = auto()
    KEYCODE_3 = auto()
    KEYCODE_4 = auto()
    KEYCODE_5 = auto()
    KEYCODE_6 = auto()
    KEYCODE_7 = auto()
    KEYCODE_8 = auto()
    KEYCODE_9 = auto()
    KEYCODE_STAR = auto()
    KEYCODE_POUND = auto()
    # KEYCODE_DPAD_UP = auto()
    # KEYCODE_DPAD_DOWN = auto()
    # KEYCODE_DPAD_LEFT = auto()
    # KEYCODE_DPAD_RIGHT = auto()
    # KEYCODE_DPAD_CENTER = auto()
    KEYCODE_VOLUME_UP = auto()
    KEYCODE_VOLUME_DOWN = auto()
    # KEYCODE_POWER = auto()
    # KEYCODE_CAMERA = auto()
    KEYCODE_CLEAR = auto()
    KEYCODE_A = auto()
    KEYCODE_B = auto()
    KEYCODE_C = auto()
    KEYCODE_D = auto()
    KEYCODE_E = auto()
    KEYCODE_F = auto()
    KEYCODE_G = auto()
    KEYCODE_H = auto()
    KEYCODE_I = auto()
    KEYCODE_J = auto()
    KEYCODE_K = auto()
    KEYCODE_L = auto()
    KEYCODE_M = auto()
    KEYCODE_N = auto()
    KEYCODE_O = auto()
    KEYCODE_P = auto()
    KEYCODE_Q = auto()
    KEYCODE_R = auto()
    KEYCODE_S = auto()
    KEYCODE_T = auto()
    KEYCODE_U = auto()
    KEYCODE_V = auto()
    KEYCODE_W = auto()
    KEYCODE_X = auto()
    KEYCODE_Y = auto()
    KEYCODE_Z = auto()
    KEYCODE_COMMA = auto()
    KEYCODE_PERIOD = auto()
    # KEYCODE_ALT_LEFT = auto()
    # KEYCODE_ALT_RIGHT = auto()
    # KEYCODE_SHIFT_LEFT = auto()
    # KEYCODE_SHIFT_RIGHT = auto()
    # KEYCODE_TAB = auto()
    KEYCODE_SPACE = auto()
    # KEYCODE_SYM = auto()
    # KEYCODE_EXPLORER = auto()
    # KEYCODE_ENVELOPE = auto()
    KEYCODE_ENTER = auto()
    KEYCODE_DEL = auto()
    # KEYCODE_GRAVE = auto()
    KEYCODE_MINUS = auto()
    KEYCODE_EQUALS = auto()
    KEYCODE_LEFT_BRACKET = auto()
    KEYCODE_RIGHT_BRACKET = auto()
    KEYCODE_BACKSLASH = auto()
    KEYCODE_SEMICOLON = auto()
    KEYCODE_APOSTROPHE = auto()
    KEYCODE_SLASH = auto()
    KEYCODE_AT = auto()
    KEYCODE_NUM = auto()
    # KEYCODE_HEADSETHOOK = auto()
    # KEYCODE_FOCUS = auto()
    KEYCODE_PLUS = auto()
    # KEYCODE_MENU = auto()
    # KEYCODE_NOTIFICATION = auto()
    # KEYCODE_SEARCH = auto()
    # TAG_LAST_KEYCOD = auto()


class UserRotation(Enum):

    '''
    possible values of User_Rotation
    '''
    ROTATION_POTRAIT = 0
    ROTATION_LANDSCAPE = 1
    ROTATION_REVERSE_POTRAIT = 2
    ROTATION_REVERSE_LANDSCAPE = 3


class Namespace(Enum):

    '''
    possible values of namespace
    '''
    SYSTEM = 'system'
    GLOBAL = 'global'
    SECURE = 'secure'


class Airplane(Enum):

    '''
    possible values of Airplane mode
    '''
    MODE_ON = 1
    MODE_OFF = 0


class AdbSettings:

    '''
        AdbSettings api - for controlling adb devices
    '''
    emulator_name = ''
    # TODO: Fix so that emulator_device is replaced by emulator.

    def __init__(self, emulator_device: str):

        emulators = api_commands.adb_list_avd_devices()
        if not emulator_device in emulators:
            util.detail_print(emulator_device)
            print('error. possible choices are: ')
            util.detail_print(emulators)
            raise ValueError()
        self.emulator_name = emulator_device

    def subprocess_call_set(self, value: str, namespace: Namespace):
        '''
            calls subprocess to set `value`
        '''
        options = [ADB, '-s', self.emulator_name,
                   'shell', 'settings', 'put', namespace.value]
        values = value.split(' ')
        options = options + values
        # print(options)
        try:
            subprocess.check_output(options)
        except subprocess.CalledProcessError as exception:
            print(exception)

    def adb_send_key_event(self, event: KeyEvent):
        '''
        sends key event to the emulator
        '''
        subprocess.check_output(
            [ADB, '-s', self.emulator_name, 'shell', 'input', 'keyevent', str(event.name)])

        # http://stackoverflow.com/questions/6236340/how-to-limit-speed-of-internet-connection-on-android-emulator

    def adb_send_key_event_test(self, event_name: str):
        '''
        sends key event to the emulator
        '''
        subprocess.check_output(
            [ADB, '-s', self.emulator_name, 'shell', 'input', 'keyevent', event_name])

    def subprocess_call_get(self, value, namespace: Namespace):
        '''
            sets a value. for example,
            >>> adb -s emulator_name shell settings get system values:
        '''
        # adb shell settings get system accelerometer_rotation
        options = [ADB, '-s', self.emulator_name,
                   'shell', 'settings', 'get', namespace.value]
        values = value.split(' ')
        options = options + values
        util.debug_print(options, flag=PRINT_FLAG)
        try:
            value = subprocess.check_output(options).decode().strip()
            print(value)
            return value
        except subprocess.CalledProcessError as exception:
            print(exception)

    def reset_all(self):
        '''
            defaults to settings.
            accelerometer_rotation on
            airplane_mode_off
            user_rotation POTRAIT
        '''
        self.set_accelerometer_rotation(False)
        self.set_user_rotation(UserRotation.ROTATION_POTRAIT)
        self.set_accelerometer_rotation(True)

    # def adb_start_server_safe(self):
    #     '''
    #     checks if `adb server` is running. if not, starts it.
    #     '''
    #     try:
    #         status = subprocess.check_output(['pidof', ADB])
    #         print('adb already running in PID: ' + status.decode())
    #         return True
    #     except subprocess.CalledProcessError as exception:
    #         print('adb is not running, returned status: ' +
    #               str(exception.returncode))

    #         print('adb was not started. starting...')

    #         try:
    #             subprocess.check_output([ADB, 'start-server'])
    #             return True
    #         except subprocess.SubprocessError as exception:
    #             print('something disastrous happened. maybe ' +
    #                   ADB + ' was not found')
    #             return False

    def get_accelerometer_rotation(self):
        '''
            gets the accelerometer rotation value
        '''
        return self.subprocess_call_get('accelerometer_rotation', Namespace.SYSTEM)

    def set_accelerometer_rotation(self, value: bool):
        '''
           sets the accelerometer rotation value
        '''
        if value:
            self.subprocess_call_set(
                'accelerometer_rotation 1', Namespace.SYSTEM)
        else:
            self.subprocess_call_set(
                'accelerometer_rotation 0', Namespace.SYSTEM)

    def set_user_rotation(self, rotation: UserRotation):
        '''
            sets user rotation based on rotation
        '''
        self.set_accelerometer_rotation(False)
        self.subprocess_call_set(
            'user_rotation ' + str(rotation.value), Namespace.SYSTEM)

    def get_airplane_mode(self) -> bool:
        '''
            gets airplane mode by `mood`
        '''
        if self.subprocess_call_get('airplane_mode_on', Namespace.GLOBAL) == '0':
            return False
        else:
            return True

    def set_airplane_mode(self, mode: Airplane):
        '''
            gets airplane mode by `mood`
        '''
        if mode == Airplane.MODE_ON:
            self.subprocess_call_set('airplane_mode_on 1',
                                     Namespace.GLOBAL)
        else:
            self.subprocess_call_set(
                'airplane_mode_on 0', Namespace.GLOBAL)


# TODO: WIFI On:
# https://developer.android.com/reference/android/provider/Settings.Global.html#WIFI_ON
