'''
mobile monkey
'''
import time
from typing import List
from threading import Thread
import config_reader as config
import emulator_manager
import api_commands
from telnet_connector import TelnetAdb
from telnet_connector import GsmProfile
from telnet_connector import NetworkDelay
from telnet_connector import NetworkStatus
from emulator import Emulator
from fuzz_context import Fuzzer
from adb_settings import Airplane, KeyEvent, UserRotation
# import adb_settings as AdbSettings
import util
from adb_monkey import AdbMonkey
from apk import Apk
from adb_logcat import Logcat, TestType, FatalWatcher
from log_analyzer import Analyzer

PRINT_FLAG = True
TIME_PRINT_FLAG = True
emulator_model = config.EMULATOR_NAME
emulator_port = config.EMULATOR_PORT
contextual_events = 0
WILL_MONKEY = True


def start_emulator() -> bool:
    '''
        starts emulator
    '''
    command = config.EMULATOR
    global emulator_model
    if emulator_manager.adb_instances_manager():
        util.debug_print('already emulators are running.', flag=PRINT_FLAG)
        return True
    else:
        util.debug_print(
            str.format("No emulator instance running. starting {} at port {}",
                       emulator_model, emulator_port), flag=PRINT_FLAG)
        api_commands.adb_start_server_safe()
        emulator_manager.emulator_start_avd(
            emulator_port, emulator_model)
        # subprocess.Popen([command,
        #                   '-port', str(emulator_port), '-avd',
        #                   emulator_name, '-use-system-libs'],
        #                  stdout=subprocess.PIPE)
        emulator_manager.check_avd_booted_completely(emulator_port)
        return True


def run(apk: Apk, emulator_name: str, emulator_port: int):
    '''
        runs things
    '''
    to_kill = False
    to_test = True

    to_full_run = True
    wipe_after_finish = True
    # test_time_seconds = 30
    if not start_emulator():
        return
    emulator = emulator_manager.get_adb_instance_from_emulators(emulator_name)
    # emulator_name = 'emulator-' + emulator.port

    # telnet_connector = TelnetAdb(config.LOCALHOST, emulator.port)
    # apk = Apk(config.APK_FULL_PATH)

    api_commands.adb_uninstall_apk(emulator, apk)

    #api_commands.decode_apk(apk)

    #api_commands.overwrite_android_manifest()

    #api_commands.build_apk(apk)

    #api_commands.sign_apk(apk)

    api_commands.adb_install_apk(emulator, apk)

    api_commands.adb_start_launcher_of_apk(emulator, apk)

    #mobicomonkey.start_test()




if __name__ == '__main__':
    run(Apk(config.APK_FULL_PATH), config.EMULATOR_NAME, config.EMULATOR_PORT)
