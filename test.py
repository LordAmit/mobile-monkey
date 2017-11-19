import config_reader as config
from  emulator  import Emulator
import api_commands
from apk import Apk
import emulator_manager
from xml.dom import minidom
from xml_element import XML_Element
from adb_settings import AdbSettings
import random

def __random_value_generator(lower_limit: int, upper_limit: int):

    if not isinstance(lower_limit, int):
        raise ValueError("lower_limit must be int")
    if not isinstance(upper_limit, int):
        raise ValueError("upper_limit must be int")
    return random.randint(lower_limit, upper_limit)

def some_method() -> str:

    apk = Apk(config.APK_FULL_PATH)
    emulator = emulator_manager.get_adb_instance_from_emulators(config.EMULATOR_NAME)
    
    '''
    file = open("activity_list", "w")
    file.write(api_commands.adb_get_activity_list(emulator, apk))
    file.close();

    file = open('activity_list', 'r')
    for l in file.readlines():
        if 'A: android:name' in l and 'Activity' in l:
            arr = l.split('"');
            print(arr[1]) 
    print(api_commands.adb_uiautomator_dump(emulator))'''

    xmldoc = minidom.parse('201711071244_dump.xml')
    element_list = []
    itemlist = xmldoc.getElementsByTagName('node')
    for s in itemlist:
        if s.attributes['class'].value in ["android.widget.EditText"]:
            bounds = s.attributes['bounds'].value.split("][")
            xpos = bounds[0][1:]
            ypos = bounds[1][:len(bounds[1])-1]
            x1 = int (xpos.split(",")[0])
            x2 = int (xpos.split(",")[1])
            y1 = int (ypos.split(",")[0])
            y2 = int (ypos.split(",")[1])
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
        rand = __random_value_generator(config.MINIMUM_INTERVAL, config.MAXIMUM_INTERVAL)
        print(rand)
        print(item.resource_id, item.xpos, item.ypos)
        api_commands.adb_input_tap(emulator, item.xpos, item.ypos)
        adb_settings = AdbSettings("emulator-"+ emulator.port)
        adb_settings.adb_send_key_event_test("KEYCODE_BACK")
        

if __name__ == '__main__':
    some_method()
