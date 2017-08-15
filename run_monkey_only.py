import time
import subprocess
import util
import api_commands
import emulator_manager
import config_reader as config
from apk import Apk
import mobile_monkey
from telnet_connector import TelnetAdb
from adb_logcat import Logcat, TestType
from log_analyzer import Analyzer


def run(apk: Apk, emulator_name: str, emulator_port: int):
    '''
        runs only monkey
    '''
    api_commands.adb_start_server_safe()
    mobile_monkey.start_emulator()
    emulator = emulator_manager.get_adb_instance_from_emulators(
        config.EMULATOR_NAME)
    # api_commands.adb_uninstall_apk(emulator, apk)
    # api_commands.adb_install_apk(emulator, apk)
    api_commands.adb_start_launcher_of_apk(emulator, apk)
    log = Logcat(emulator, apk, TestType.Monkey)
    log.start_logcat()
    telnet_connector = TelnetAdb(config.LOCALHOST, emulator.port)
    print("Monkey started at: {}".format(time.ctime()))
    subprocess.check_call([
        config.adb, 'shell', 'monkey',
        '-p', apk.package_name,
        '--throttle', config.MONKEY_INTERVAL,
        '-s', str(config.SEED),
        '-v', '-v', '-v',
        str(config.DURATION)])
    print("Monkey stopped at: {}".format(time.ctime()))
    api_commands.adb_stop_activity_of_apk(emulator, apk)
    log.stop_logcat()
    analyzer = Analyzer(log.file_address)
    print(analyzer)
    api_commands.adb_uninstall_apk(emulator, apk)
    # telnet_connector.kill_avd()
    # emulator_manager.emulator_wipe_data(emulator)

if __name__ == '__main__':

    run(Apk(config.APK_FULL_PATH), config.EMULATOR_NAME, config.EMULATOR_PORT)
