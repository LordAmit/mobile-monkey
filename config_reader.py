"""
config_reader module
"""

import configparser as ConfigParser
import util
import os
"""
ConfigReader takes care of config file reading
"""


def get(value: str):
    """
    :rtype: str
    :param value: available options are directory, uploads, projects,
    :return: string that contains value from config file.
    """
    config = ConfigParser.ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'configFile'))
    return config.get('emulator', value)


TELNET_KEY = get("telnet_key")
LOCALHOST = get("localhost")
directory = get("directory")
# apk = get("apk")
# apk_unaligned = get("apk_unaligned")
# apk_test_unaligned = get("apk_test_unaligned")
adb = get("adb")
# avds = get("avds")
emulator = get("emulator")
# test_class = get("test_class")
# test_method = get("test_method")
# SERVER_FILE_ADDRESS = get("server_file_address")
# SERVER_FILE_PORT = get("server_file_port")
TEMP = get("temp")
CURRENT_DIRECTORY = get("current_directory")
# UID = get("uid")
# PROJECT_NAME = get("project_name")
EMULATOR = get("emulator")
MINIMUM_INTERVAL = int(get("minimum_interval"))
MAXIMUM_INTERVAL = int(get("maximum_interval"))
SEED = int(get("seed"))
DURATION = int(get("duration"))
# APP_PACKAGE_NAME = get("app_package_name")
UNIFORM_INTERVAL = int(get("uniform_interval"))
APK_FULL_PATH = get("apk_full_path")
AAPT = get("aapt")
EMULATOR_NAME = get("emulator_name")
EMULATOR_PORT = get("emulator_port")
LOG_ADDRESS = get("log_address")
SAMPLE_LOG = get("sample_log")
MONKEY_INTERVAL = get("monkey_interval")
MONKEY_LOG = get("monkey_log")
MOBILE_MONKEY_LOG = get("mobile_monkey_log")
DUMP_ADDRESS = get("dump_address")
HEADLESS = util.StringToBoolean((get("headless")))

# def avd_file_reader():
#     """
#     returns the list of avds
#     """
#     txt = open(avds)
#     print(txt)
#     list_avds = txt.read().split('\n')
#     print(list_avds)
#     return list_avds
