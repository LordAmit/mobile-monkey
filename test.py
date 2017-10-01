import config_reader as config
from emulator import Emulator as emulator
import api_commands
import adb_settings
import emulator_manager

emulators = emulator_manager.get_list_emulators()
# print(emulators[0])

# api_commands.adb_input_tap(emulators[0], 1200, 1900)
api_commands.adb_uiautomator_dump(emulators[0])