'''
    monkey
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

def threads_to_run(emulator: Emulator, apk: Apk, fuzz: Fuzzer) -> List:
    '''
        runs the threads after checking permissions.
    '''
    threads = []

    emulator_name = 'emulator-' + emulator.port

    if "android.permission.INTERNET" in apk.permissions or \
            "android.permission.ACCESS_NETWORK_STATE" in apk.permissions:
        network_delay_interval_events = fuzz.generate_step_interval_event(
            NetworkDelay)
        
        threads.append(Thread(target=fuzz.random_network_delay, args=(
            config.LOCALHOST, emulator, network_delay_interval_events)))
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
        gsm_profile_interval_events = fuzz.generate_step_uniforminterval_event(
            GsmProfile)

        threads.append(Thread(target=fuzz.random_gsm_profile, args=(
            config.LOCALHOST, emulator, config.UNIFORM_INTERVAL, gsm_profile_interval_events)))

    return threads


def run(emulator : Emulator, apk: Apk, emulator_name: str, emulator_port: int, seed: int, log : Logcat):
    '''
        runs things
    '''
    #telnet_connector = TelnetAdb(config.LOCALHOST, config.EMULATOR_PORT)

    fuzz = Fuzzer(config.MINIMUM_INTERVAL,
                  config.MAXIMUM_INTERVAL, seed, config.DURATION, FatalWatcher(log.file_address))
    
    threads = threads_to_run(emulator, apk, fuzz)
    
    [thread.start() for thread in threads]

    [thread.join() for thread in threads]
