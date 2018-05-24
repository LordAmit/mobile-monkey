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
from adb_settings import Airplane, KeyboardEvent, UserRotation
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
    global emulator_model
    if emulator_manager.adb_instances_manager():
        util.debug_print('already emulators are running.', flag=PRINT_FLAG)
        return True
    else:
        util.debug_print(
            str.format("No emulator instance running. starting {} at port {}",
                       emulator_model, emulator_port), flag=PRINT_FLAG)
        api_commands.adb_start_server_safe()
        emulator_manager.emulator_start_avd(emulator_port, emulator_model)
        # subprocess.Popen([command,
        #                   '-port', str(emulator_port), '-avd',
        #                   emulator_name, '-use-system-libs'],
        #                  stdout=subprocess.PIPE)
        emulator_manager.check_avd_booted_completely(emulator_port)
        return True


def threads_to_run(emulator: Emulator, apk: Apk, fuzz: Fuzzer,
                   will_monkey: bool) -> List:
    '''
        runs the threads after checking permissions.
    '''
    threads = []
    global contextual_events
    util.debug_print(apk.permissions, flag=PRINT_FLAG)
    emulator_name = 'emulator-' + str(emulator.port)
    if "android.permission.INTERNET" in apk.permissions or \
            "android.permission.ACCESS_NETWORK_STATE" in apk.permissions:
        util.debug_print("Internet permission detected", flag=PRINT_FLAG)
        network_delay_interval_events = fuzz.generate_step_interval_event(
            NetworkDelay)
        # print(network_delay_interval_events)
        contextual_events += len(network_delay_interval_events)
        threads.append(Thread(target=fuzz.random_network_delay, args=(
            config.LOCALHOST, emulator, network_delay_interval_events)))
        network_speed_interval_event = fuzz.generate_step_interval_event(
            NetworkStatus)
        # print(network_speed_interval_event)
        contextual_events += len(network_speed_interval_event)
        threads.append(Thread(target=fuzz.random_network_speed, args=(
            config.LOCALHOST, emulator, network_speed_interval_event)))

        airplane_mode_interval_events = fuzz.generate_step_interval_event(
            Airplane)
        # print(airplane_mode_interval_events)
        contextual_events += len(airplane_mode_interval_events)
        threads.append(Thread(
            target=fuzz.random_airplane_mode_call,
            args=(emulator_name, airplane_mode_interval_events)))

    if "android.permission.ACCESS_NETWORK_STATE" in apk.permissions:
        util.debug_print("access_network_state detected", flag=PRINT_FLAG)
        gsm_profile_interval_events = fuzz.generate_step_uniforminterval_event(
            GsmProfile)
        contextual_events += len(gsm_profile_interval_events)
        threads.append(Thread(target=fuzz.random_gsm_profile, args=(
            config.LOCALHOST, emulator,
            config.UNIFORM_INTERVAL, gsm_profile_interval_events)))

    user_rotation_interval_events = fuzz.generate_step_interval_event(
        UserRotation)
    contextual_events += len(user_rotation_interval_events)
    threads.append(Thread(
        target=fuzz.random_rotation, args=((emulator_name,
                                            user_rotation_interval_events))))

    key_event_interval_events = fuzz.generate_step_interval_event(
        KeyboardEvent)
    contextual_events += len(key_event_interval_events)
    threads.append(Thread(
        target=fuzz.random_key_event, args=((emulator_name,
                                             key_event_interval_events))))
    if will_monkey:
        monkey = AdbMonkey(emulator, apk,
                           config.SEED, config.DURATION)
        thread_monkey = Thread(target=monkey.start_monkey)

        threads.append(thread_monkey)
    return threads


def run(apk: Apk, emulator_name: str, emulator_port: int):
    '''
        runs things
    '''
    to_kill = False
    to_test = True

    to_full_run = True
    wipe_after_finish = False
    # test_time_seconds = 30
    if not start_emulator():
        return
    emulator = emulator_manager.get_adb_instance_from_emulators(emulator_name)
    # emulator_name = 'emulator-' + emulator.port

    telnet_connector = TelnetAdb(config.LOCALHOST, emulator.port)
    # apk = Apk(config.APK_FULL_PATH)
    # api_commands.adb_uninstall_apk(emulator, apk)
    # api_commands.adb_install_apk(emulator, apk)

    # api_commands.adb_start_launcher_of_apk(emulator, apk)
    log = Logcat(emulator, apk, TestType.MobileMonkey)

    # api_commands.adb_pidof_app(emulator, apk)

    if to_kill:
        telnet_connector.kill_avd()
        quit()
    if not to_test:
        return

    log.start_logcat()

    fuzz = Fuzzer(config.MINIMUM_INTERVAL,
                  config.MAXIMUM_INTERVAL, config.SEED,
                  config.DURATION, FatalWatcher(log.file_address))
    # log.experimental_start_logcat(fuzz)
    # fuzz.print_intervals_events()
    threads = threads_to_run(emulator, apk, fuzz, WILL_MONKEY)
    # log_thread = Thread(target=log.start, args=(fuzz,))
    global contextual_events
    print("Total contextual events: " + str(contextual_events))
    # print(threads)
    # return
    # device = AdbSettings.AdbSettings('emulator-' + adb_instance.port)
    # triggers = [fuzz.set_continue_network_speed,
    #             fuzz.set_continue_gsm_profile,
    #             fuzz.set_continue_network_delay]
    # thread_test = Thread(target=time_to_test, args=[
    #     test_time_seconds, triggers, ])

    # thread_fuzz_delay = Thread(target=fuzz.random_network_delay, args=(
    #     config.LOCALHOST, emulator.port,))
    # thread_fuzz_profile = Thread(target=fuzz.random_gsm_profile, args=(
    #     config.LOCALHOST, emulator.port, 12,))
    # thread_fuzz_speed = Thread(target=fuzz.random_network_speed, args=(
    #     config.LOCALHOST, emulator.port,))
    # thread_fuzz_rotation = Thread(
    #     target=fuzz.random_rotation, args=((emulator_name,)))
    # thread_fuzz_airplane = Thread(
    #     target=fuzz.random_airplane_mode_call, args=(emulator_name,))
    # monkey = AdbMonkey(emulator, config.APP_PACKAGE_NAME,
    #                    config.SEED, config.DURATION)
    # thread_monkey = Thread(target=monkey.start_monkey)
    if to_full_run:

        util.debug_print(
            "started testing at {}".format(time.ctime()), flag=TIME_PRINT_FLAG)
        [thread.start() for thread in threads]
        # log_thread.start()

        [thread.join() for thread in threads]
        # log.log_process.kill()
        # log.stop_logcat()
        # log_thread.join()
    # thread_monkey.start()
    # thread_fuzz_rotation.start()
    # thread_fuzz_delay.start()
    # thread_fuzz_profile.start()
    # thread_fuzz_speed.start()
    # thread_fuzz_airplane.start()
    # thread_test.start()
    # thread_test.join()
    # thread_fuzz_delay.join()
    # thread_fuzz_profile.join()
    # thread_fuzz_speed.join()
    # thread_fuzz_rotation.join()
    # thread_fuzz_airplane.join()
    # thread_monkey.join()
    # telnet_connector.kill_avd()
    api_commands.adb_stop_activity_of_apk(emulator, apk)
    log.stop_logcat()
    api_commands.adb_uninstall_apk(emulator, apk)
    util.debug_print(
        'Finished testing and uninstalling app at {}'.format(time.ctime()),
        flag=TIME_PRINT_FLAG)
    print(Analyzer(log.file_address))
    if wipe_after_finish:
        print("successfully completed testing app. Closing emulator")
        telnet_connector.kill_avd()
        emulator_manager.emulator_wipe_data(emulator)


if __name__ == '__main__':
    import os

    dir = os.path.dirname(__file__)

    StopFlagWatcher = os.path.join(dir, 'test/StopFlagWatcher')

    file = open(StopFlagWatcher, 'w')
    file.truncate()
    file.close()
    run(Apk(config.APK_FULL_PATH), config.EMULATOR_NAME, config.EMULATOR_PORT)
