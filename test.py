import config_reader as config
from  emulator  import Emulator
import api_commands
from apk import Apk
import emulator_manager
from xml.dom import minidom
from xml_element import XML_Element
from adb_settings import AdbSettings
import random
from typing import List
from threading import Thread
from adb_settings import KeyboardEvent
import enum

def __random_value_generator(lower_limit: int, upper_limit: int):

    if not isinstance(lower_limit, int):
        raise ValueError("lower_limit must be int")
    if not isinstance(upper_limit, int):
        raise ValueError("upper_limit must be int")
    return random.randint(lower_limit, upper_limit)

def some_method() -> str:

    apk = Apk(config.APK_FULL_PATH)
    emulator = emulator_manager.get_adb_instance_from_emulators(config.EMULATOR_NAME)
    adb_settings = AdbSettings("emulator-" + emulator.port)
    activities = []

    
    
    file = open("activity_list", "w")
    file.write(api_commands.adb_get_activity_list(emulator, apk))
    file.close();

    file = open('activity_list', 'r')
    for l in file.readlines():
        if 'A: android:name' in l and 'Activity' in l:
            arr = l.split('"')
            activities.append(arr[1])
            print(arr[1])

    for activity in activities:
        api_commands.adb_start_activity(emulator, apk, activity)
        print(api_commands.adb_uiautomator_dump(emulator))
        xmldoc = minidom.parse(api_commands.adb_uiautomator_dump(emulator))
        element_list = []
        itemlist = xmldoc.getElementsByTagName('node')
        for s in itemlist:
            if s.attributes['class'].value in ["android.widget.EditText"]:
                bounds = s.attributes['bounds'].value.split("][")
                Lpos = bounds[0][1:]
                Rpos = bounds[1][:len(bounds[1])-1]
                x1 = int (Lpos.split(",")[0])
                y1 = int (Lpos.split(",")[1])
                x2 = int (Rpos.split(",")[0])
                y2 = int (Rpos.split(",")[1])
                x = XML_Element(s.attributes['resource-id'].value,
                            s.attributes['class'].value,
                            s.attributes['checkable'].value,
                            s.attributes['checked'].value,
                            s.attributes['clickable'].value,
                            s.attributes['enabled'].value,
                            s.attributes['focusable'].value,
                            s.attributes['focused'].value,
                            s.attributes['scrollable'].value,
                            s.attributes['long-clickable'].value,
                            s.attributes['password'].value,
                            s.attributes['selected'].value,
                            (x1+x2)/2,
                            (y1+y2)/2)
                element_list.append(x)

        for item in element_list:
            print(item.resource_id, item.xpos, item.ypos)
            api_commands.adb_input_tap(emulator, item.xpos, item.ypos)
            rand = random.randint(5, 10)
            for i in range(rand):
                KeyCode = KeyboardEvent(random.randint(0, 40)).name
                print("Sending event " + KeyCode)
                adb_settings.adb_send_key_event_test(KeyCode)
            adb_settings.adb_send_key_event_test("KEYCODE_BACK")

if __name__ == '__main__':
    some_method()
