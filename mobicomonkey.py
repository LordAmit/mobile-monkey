import config_reader as config
from emulator import Emulator
import api_commands
from apk import Apk
import emulator_manager
from xml.dom import minidom  # type: ignore
from xml_element import XML_Element
from adb_settings import AdbSettings
from telnet_connector import TelnetAdb
import random
from typing import List
from threading import Thread
from adb_settings import KeyboardEvent
import os
import util
import monkey
from adb_logcat import Logcat, TestType
import mutex
eventlog = open('test/EventLog', 'w')


def reset_emulator(
        host: str = config.LOCALHOST,
        emulator_port: str = config.EMULATOR_PORT):
    print("resetting emulator")
    adb_device = AdbSettings("emulator-" + str(emulator_port))
    telnet_object = TelnetAdb(host, int(emulator_port))
    adb_device.reset_all()
    telnet_object.reset_all()


def start_test():

    apk = Apk(config.APK_FULL_PATH)

    emulator = emulator_manager.get_adb_instance_from_emulators(
        config.EMULATOR_NAME)
    adb_settings = AdbSettings("emulator-" + str(emulator.port))
    activities = []

    log = Logcat(emulator, apk, TestType.MobileMonkey)

    log.start_logcat()

    if config.GUIDED_APPROACH == 1:
        file = open('test/activity_list', 'r')
        for l in file.readlines():
            activities.append(l.strip())
            print(l.strip())
        file.close()

    else:
        file = open("test/activity", "w")
        file.write(api_commands.adb_get_activity_list(emulator, apk))
        file.close()

        file = open('test/activity', 'r')
        file2 = open('test/activity_list', 'w')

        for l in file.readlines():
            if 'A: android:name' in l and 'Activity' in l:
                arr = l.split('"')
                activities.append(arr[1])
                file2.write(arr[1] + "\n")
                print(arr[1])
        file.close()
        file2.close()
        os.remove('test/activity')

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
            emulator, apk, config.EMULATOR_NAME, config.EMULATOR_PORT,
            seed, log)))

        # monkey.run(emulator, apk, config.EMULATOR_NAME,
        # config.EMULATOR_PORT, seed, log)

        threads.append(Thread(target=test_ui, args=(
            activity, emulator, adb_settings, display_height)))

        [thread.start() for thread in threads]

        [thread.join() for thread in threads]

        seed = seed + 1

    log.stop_logcat()
    eventlog.close()


def force_update_element_list(emulator: Emulator, adb_settings: AdbSettings):
    print("found mutex = " + str(mutex.ROTATION_MUTEX))
    print("element list force update here.")
    element_list = get_elements_list(emulator, adb_settings)
    mutex.ROTATION_MUTEX = 0
    print("reset the MUTEX after update.")
    return element_list


def test_ui(activity: str, emulator: Emulator, adb_settings: AdbSettings,
            display_height: str):

    file = open('test/StopFlagWatcher', 'w')
    file.truncate()

    element_list = get_elements_list(emulator, adb_settings)

    while len(element_list) > 0:
        traverse_elements(activity, element_list, emulator, adb_settings)
        previous_elements = element_list
        api_commands.adb_display_scroll("{}".format(
            int(display_height) - int(display_height) / 10))
        element_list = get_elements_list(emulator, adb_settings)
        element_list = element_list_compare(previous_elements, element_list)

    file.write("1")


def element_list_compare(previous_elements: List[XML_Element],
                         current_elements: List[XML_Element]):
    for previous_item in previous_elements:
        for current_item in current_elements:
            if previous_item.resource_id == current_item.resource_id:
                print('matched')
                current_elements.remove(current_item)
    return current_elements


def traverse_elements(activity: str, element_list: List[XML_Element],
                      emulator: Emulator, adb_settings: AdbSettings):
    for i in range(0, len(element_list)):
        if(mutex.ROTATION_MUTEX):
            element_list = element_list_compare(element_list[0:i],
                                                force_update_element_list(
                                                    emulator, adb_settings))
            for j in range(0, len(element_list)):
                input_key_event(
                    activity, element_list[j], emulator, adb_settings)
            break
        # print(item.resource_id, item.xpos, item.ypos)
        input_key_event(activity, element_list[i], emulator, adb_settings)


def input_key_event(activity: str, item: XML_Element,
                    emulator: Emulator, adb_settings: AdbSettings):
    api_commands.adb_input_tap(emulator, item.xpos, item.ypos)
    rand = random.randint(config.MINIMUM_KEYEVENT, config.MAXIMUM_KEYEVENT)
    for i in range(rand):
        KeyCode = KeyboardEvent(random.randint(0, 40)).name
        print("Sending event " + KeyCode)
        adb_settings.adb_send_key_event_test(KeyCode)
        eventlog.write(util.return_current_time_in_logcat_style() + '\t' +
                       activity + '\t' + item.resource_id +
                       '\t' + KeyCode + '\n')
    adb_settings.adb_send_key_event_test("KEYCODE_BACK")


def get_elements_list(emulator: Emulator, adb_settings: AdbSettings) -> List:
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
    reset_emulator()
