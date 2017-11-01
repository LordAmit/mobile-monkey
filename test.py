import config_reader as config
from  emulator  import Emulator
import api_commands
from apk import Apk
import emulator_manager

def some_method() -> str:

    apk = Apk(config.APK_FULL_PATH)
    emulator = emulator_manager.get_adb_instance_from_emulators(config.EMULATOR_NAME)
    
    file = open("activity_list", "w")
    file.write(api_commands.adb_get_activity_list(emulator, apk))
    file.close();

    file = open('activity_list', 'r')
    for l in file.readlines():
        if 'A: android:name' in l and 'Activity' in l:
            arr = l.split('"');
            print(arr[1])
        

if __name__ == '__main__':
    some_method()