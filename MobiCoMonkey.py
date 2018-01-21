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
import os
import util
import monkey
from adb_logcat import Logcat, TestType
import subprocess

eventlog = open('EventLog', 'w')

def start_test() -> str:

    apk = Apk(config.APK_FULL_PATH)

    emulator = emulator_manager.get_adb_instance_from_emulators(config.EMULATOR_NAME)
    adb_settings = AdbSettings("emulator-" + emulator.port)
    activities = []

    log = Logcat(emulator, apk, TestType.MobileMonkey)

    log.start_logcat()

    if config.GUIDED_APPROACH == 1:
        file = open('activity_list', 'r')
        for l in file.readlines():
            activities.append(l.strip())
            print(l.strip())
        file.close()

    else:
        file = open("activity", "w")
        file.write(api_commands.adb_get_activity_list(emulator, apk))
        file.close()

        file = open('activity', 'r')
        file2 = open('activity_list', 'w')

        for l in file.readlines():
            if 'A: android:name' in l and 'Activity' in l:
                arr = l.split('"')
                activities.append(arr[1])
                file2.write(arr[1] +"\n")
                print(arr[1])
        file.close()
        file2.close()
        os.remove('activity')
        
    print(len(activities))

    display_properties = api_commands.adb_display_properties().decode()
    if 'DisplayDeviceInfo' in display_properties:
        arr = display_properties.split('height=')[1]
        display_height = arr.split(',')[0]

    seed = config.SEED

    for activity in activities:
        
        try:
            api_commands.adb_start_activity(emulator, apk, activity)
        except Exception:
            print(Exception)

        threads = []

        threads.append(Thread(target=monkey.run, args=(
            emulator, apk, config.EMULATOR_NAME, config.EMULATOR_PORT, seed, log)))

        #monkey.run(emulator, apk, config.EMULATOR_NAME, config.EMULATOR_PORT, seed, log)

        threads.append(Thread(target=test_ui, args=(activity, emulator, adb_settings, display_height)))

        [thread.start() for thread in threads]

        [thread.join() for thread in threads]

        seed = seed + 1

    log.stop_logcat()
    eventlog.close()

def test_ui(activity: str, emulator : Emulator, adb_settings : AdbSettings, display_height: str):

    file = open('StopFlagWatcher', 'w')
    file.truncate()

    element_list = get_elements_list(emulator, adb_settings)

    while len(element_list) > 0:
        input_key_event(activity, element_list, emulator, adb_settings)
        previous_elements = element_list
        api_commands.adb_display_scroll("{}".format(int(display_height) - int(display_height) / 10))
        element_list = get_elements_list(emulator, adb_settings)
        element_list = element_list_compare(previous_elements, element_list)

    file.write("1")

def element_list_compare(previous_elements : XML_Element, current_elements : XML_Element):
    for previous_item in previous_elements:
        for current_item in current_elements:
            if previous_item.resource_id == current_item.resource_id:
                print('matched')
                current_elements.remove(current_item)
    return current_elements


def input_key_event(activity: str, element_list: XML_Element, emulator: Emulator, adb_settings: AdbSettings):
    for item in element_list:
        print(item.resource_id, item.xpos, item.ypos)
        api_commands.adb_input_tap(emulator, item.xpos, item.ypos)
        rand = random.randint(config.MINIMUM_KEYEVENT, config.MAXIMUM_KEYEVENT)
        for i in range(rand):
            KeyCode = KeyboardEvent(random.randint(0, 40)).name
            print("Sending event " + KeyCode)
            adb_settings.adb_send_key_event_test(KeyCode)
            eventlog.write(util.return_current_time_in_logcat_style() + '\t' + activity + '\t' + item.resource_id +
                           '\t' + KeyCode + '\n')
        adb_settings.adb_send_key_event_test("KEYCODE_BACK")

def get_elements_list(emulator : Emulator, adb_settings : AdbSettings) -> List:
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
    return element_list

if __name__ == '__main__':
    start_test()
