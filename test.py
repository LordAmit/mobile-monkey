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


def some_method() -> str:

    apk = Apk(config.APK_FULL_PATH)
    emulator = emulator_manager.get_adb_instance_from_emulators(config.EMULATOR_NAME)
    adb_settings = AdbSettings("emulator-" + emulator.port)
    activities = []
    
    file = open("activity_list", "w")
    file.write(api_commands.adb_get_activity_list(emulator, apk))
    file.close()

    file = open('activity_list', 'r')
    for l in file.readlines():
        if 'A: android:name' in l and 'Activity' in l:
            arr = l.split('"')
            activities.append(arr[1])
            print(arr[1])

    result = api_commands.adb_display_properties().decode()
    if 'DisplayDeviceInfo' in result:
        arr = result.split('height=')[1]
        display_height = arr.split(',')[0]

    for activity in activities:
        previous_elements = []
        api_commands.adb_start_activity(emulator, apk, activity)
        element_list = test(emulator,adb_settings)

        while len(set(previous_elements).intersection(element_list)) >0 :
            previous_elements = element_list
            api_commands.adb_display_scroll("{}".format(int(display_height) - int(display_height) / 10))
            element_list = test(emulator,adb_settings)

def test(emulator : Emulator, adb_settings : AdbSettings) -> List:
    xmldoc = minidom.parse(api_commands.adb_uiautomator_dump(emulator))
    element_list = []
    itemlist = xmldoc.getElementsByTagName('node')
    for s in itemlist:
        if s.attributes['class'].value in ["android.widget.EditText"]:
            bounds = s.attributes['bounds'].value.split("][")
            Lpos = bounds[0][1:]
            Rpos = bounds[1][:len(bounds[1]) - 1]
            x1 = int(Lpos.split(",")[0])
            y1 = int(Lpos.split(",")[1])
            x2 = int(Rpos.split(",")[0])
            y2 = int(Rpos.split(",")[1])
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
                            (x1 + x2) / 2,
                            (y1 + y2) / 2)
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

    return element_list

if __name__ == '__main__':    
    some_method()
