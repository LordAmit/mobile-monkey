'''
    monkey
'''
from threading import Thread
from typing import List

import config_reader as config
from adb_logcat import FatalWatcher, Logcat
from apk import Apk
from emulator import Emulator
from fuzz_context import Fuzzer
from adb_settings import Airplane
from telnet_connector import GsmProfile, NetworkDelay, NetworkStatus
import interval_event
PRINT_FLAG = True
TIME_PRINT_FLAG = True


def threads_to_run(emulator: Emulator, apk: Apk, fuzz: Fuzzer) -> List:
    '''
        runs the threads after checking permissions.
    '''
    threads = []

    emulator_name = 'emulator-' + str(emulator.port)

    if "android.permission.INTERNET" in apk.permissions or \
            "android.permission.ACCESS_NETWORK_STATE" in apk.permissions:
        if config.GUIDED_APPROACH == 1:
            network_delay_interval_events =\
                interval_event.read_interval_event_from_file(
                    'test/networkdelay.txt', NetworkDelay)
        else:
            network_delay_interval_events = fuzz.generate_step_interval_event(
                NetworkDelay)

        threads.append(Thread(target=fuzz.random_network_delay, args=(
            config.LOCALHOST, emulator, network_delay_interval_events)))

        if config.GUIDED_APPROACH == 1:
            network_speed_interval_event =\
                interval_event.read_interval_event_from_file(
                    'test/networkstatus.txt', NetworkStatus)
        else:
            network_speed_interval_event = fuzz.generate_step_interval_event(
                NetworkStatus)

        threads.append(Thread(target=fuzz.random_network_speed, args=(
            config.LOCALHOST, emulator, network_speed_interval_event)))
        airplane_mode_interval_events = fuzz.generate_step_interval_event(
            Airplane)

        threads.append(Thread(
            target=fuzz.random_airplane_mode_call,
            args=(emulator_name, airplane_mode_interval_events)))

    if "android.permission.ACCESS_NETWORK_STATE" in apk.permissions:

        if config.GUIDED_APPROACH == 1:
            gsm_profile_interval_events = \
                interval_event.read_interval_event_from_file(
                    'test/gsmprofile.txt', GsmProfile)
        else:
            gsm_profile_interval_events = fuzz.generate_step_interval_event(
                GsmProfile)

        threads.append(Thread(target=fuzz.random_gsm_profile, args=(
            config.LOCALHOST, emulator, config.UNIFORM_INTERVAL,
            gsm_profile_interval_events)))

    return threads


def run(emulator: Emulator, apk: Apk, emulator_name: str, emulator_port: int,
        seed: int, log: Logcat):
    '''
        runs things
    '''
    # telnet_connector = TelnetAdb(config.LOCALHOST, config.EMULATOR_PORT)

    fuzz = Fuzzer(config.MINIMUM_INTERVAL,
                  config.MAXIMUM_INTERVAL, seed, config.DURATION,
                  FatalWatcher(log.file_address))

    threads = threads_to_run(emulator, apk, fuzz)

    [thread.start() for thread in threads]

    [thread.join() for thread in threads]
