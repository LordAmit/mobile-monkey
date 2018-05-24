'''
adb monkey interface
'''
import subprocess
import time
import config_reader as config
import api_commands
from emulator import Emulator
from apk import Apk
PRINT_FLAG = False


class AdbMonkey:

    '''
    AdbMonkey executes the monkey adb tool
    '''
    adb = config.adb

    def __init__(self, emulator: Emulator, apk: Apk, seed: int,
                 number_of_events: int)-> None:

        api_commands.adb_start_server_safe()
        if seed > 500 or seed < 0:
            raise ValueError("seed must be within the range of 0 to 500")
        if number_of_events > 4200 or number_of_events < 10:
            raise ValueError(
                "number of events must be at least 10 seconds and at most 4200")
        # adb shell pm list packages | grep com.ebooks.ebookreader
        self.number_of_events = number_of_events
        self.seed = seed
        # output = subprocess.check_output(
        #     [self.adb, 'shell', 'pm', 'list', 'packages', '|', 'grep',
        #      app_package_name]).decode().strip().split('\r\n')
        # util.debug_print(output, len(output), flag=PRINT_FLAG)
        output = api_commands.adb_is_package_present(
            emulator, apk.package_name)
        if output < 1:
            raise ValueError("Provided {} not found.".format(apk.package_name))
        elif output > 1:
            raise ValueError(
                "Provided {} is too unspecific," +
                " multiple entries found.".format(apk.package_name))
        self.app_package_name = apk.package_name

    def start_monkey(self):
        '''
        starts monkey
        '''
        # adb shell monkey -p com.eatl.appstore -v -v -v -s 314 --throttle
        # 1000 100
        subprocess.check_call([
            self.adb, 'shell', 'monkey',
            '-p', self.app_package_name,
            '--throttle', config.MONKEY_INTERVAL,
            # '--pct-touch', '60',
            # '--pct-trackball', '20',
            # '--pct-motion', '20',
            '-s', str(self.seed),
            '-v', '-v', '-v',
            str(self.number_of_events)])
        print('Monkey finished at: {}'.format(time.ctime()))


def main():
    import config_reader as config
    from apk import Apk
    from adb_settings import AdbSettings
    import emulator_manager
    from adb_logcat import Logcat, TestType
    # print("resetting emulator")
    import os
    import api_commands

    activities = []
    apk = Apk(config.APK_FULL_PATH)
    emulator = emulator_manager.get_adb_instance_from_emulators(
        config.EMULATOR_NAME)
    file = open("test/activity", "w")
    file.write(api_commands.adb_get_activity_list(emulator, apk))
    file.close()

    file = open('test/activity', 'r')
    file2 = open('test/activity_list', 'w')

    for l in file.readlines():
        if 'A: android:name' in l and 'Activity' in l:
            arr = l.split('"')
            activities.append(arr[1])
            file2.write(arr[1] + "\n")
            print(arr[1])
    file.close()
    file2.close()
    os.remove('test/activity')

    # log = Logcat(emulator, apk, TestType.MobileMonkey)
    # log.start_logcat()
    AdbMonkey(emulator, apk, config.SEED, config.DURATION*10).start_monkey()
    # log.stop_logcat()


if __name__ == '__main__':
    main()
