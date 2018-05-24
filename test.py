import os
import api_commands
import emulator_manager
import config_reader as config
from apk import Apk
import api_commands
from adb_logcat import Logcat, TestType

activities = []
apk = Apk(config.APK_FULL_PATH)
emulator = emulator_manager.get_adb_instance_from_emulators(
    config.EMULATOR_NAME)
# file = open("test/activity", "w")
# file.write(api_commands.adb_get_activity_list(emulator, apk))
# file.close()

# file = open('test/activity', 'r')
# file2 = open('test/activity_list', 'w')

# for l in file.readlines():
#     if 'A: android:name' in l and 'Activity' in l:
#         arr = l.split('"')
#         activities.append(arr[1])
#         file2.write(arr[1] + "\n")
#         print(arr[1])
# file.close()
# file2.close()
# os.remove('test/activity')
from telnet_connector import TelnetAdb
import adb_monkey
from adb_logcat import Logcat
from threading import Thread
from typing import List
import os
import config_reader as config
from adb_logcat import FatalWatcher, Logcat
from apk import Apk
from emulator import Emulator
from fuzz_context import Fuzzer
from adb_settings import Airplane, UserRotation
from telnet_connector import GsmProfile, NetworkDelay, NetworkStatus
import interval_event

PRINT_FLAG = True

dir = os.path.dirname(__file__)
network_delay = os.path.join(dir, 'test/networkdelay.txt')
network_status = os.path.join(dir, 'test/networkstatus.txt')
gsm_profile = os.path.join(dir, 'test/gsmprofile.txt')
print(network_delay)
print(network_status)
threads = []

log = Logcat(emulator, apk, TestType.MobileMonkey)

fuzz = Fuzzer(config.MINIMUM_INTERVAL,
              config.MAXIMUM_INTERVAL, config.SEED, config.DURATION,
              FatalWatcher(log.file_address))

# if config.CONTEXT_FILE == 1:
#     network_delay_interval_events =\
#         interval_event.read_interval_event_from_file(
#             network_delay, NetworkDelay)
# else:
# network_delay_interval_events = fuzz.generate_step_interval_event(
#     NetworkDelay)
# threads.append(Thread(target=fuzz.random_network_delay, args=(
#     config.LOCALHOST, emulator, network_delay_interval_events)))

tel = TelnetAdb()
tel.set_gsm_profile(GsmProfile.STRENGTH4)
# [thread.start() for thread in threads]
# [thread.join() for thread in threads]
# emulator_mana11ger.emulator_wipe_data(emulator)
