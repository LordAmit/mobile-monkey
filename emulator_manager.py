'''
Emulator Manager
'''

import subprocess

from subprocess import Popen, PIPE
import syslog
import time
import os
from typing import List
from emulator import Emulator
import config_reader as config
from contextConfig_reader import ContextConfigReader as c_config
import api_commands
import util
emulator_processes = []

context_list = {}

PRINT_FLAG = False


def get_context(uid: str= "mostaque#1485838365"):
    '''
        gets the full contexts from contextConfigFile from specified project
    '''
    list1 = ['emulator_name', 'abi', 'android_version',
             'net_speed', 'net_delay', 'cpu_delay', 'Screen_orientation']
    i = 0
    for items in list1:
        command = c_config.context_config_reader(str(list1[i]), uid)
        context_list.update({list1[i]: command})
        i += 1
    print(context_list)
    return context_list


def create_emulator():
    android = config.get('android')
    target_id = 5
    emulator_create = subprocess.Popen(
        [android, 'create', 'avd', '-n', context_list['emulator_name'], '-t', str(target_id), '-b',
         context_list['abi']], stdin=subprocess.PIPE)
    stri = str('n').encode('utf-8')
    emulator_create.stdin.write(stri)
    return emulator_create


def get_avd_list():
    '''
    returns a list of avds
    '''
    return api_commands.emulator_list_of_avds()


def get_running_avd_ports() -> List:
    '''
    returns a list containing ports of running avds
    '''
    return api_commands.adb_list_avd_ports()


def kill_emulator():
    android = config.get('android')
    process = subprocess.Popen(
        [android, 'delete', 'avd', '-n', context_list['emulator_name']])


def check_avd_booted_completely(emulator_port) -> str:
    """
    Checks if the AVD specified in ``port`` is booted completely through a system call:
    >>> adb -s emulator-5555  shell getprop sys.boot_completed
    it returns 1 if boot is completed.

    args:

            emulator_port (int): The port of the emulator

    returns:

            if completed, returns 1. Otherwise, continues checking.

    """
    port = "emulator-"
    port = port + str(emulator_port)

    adb = config.adb
    print(port)
    print("going to sleep")
    time.sleep(20)
    i = 0
    while True:
        check = subprocess.check_output(
            [adb, '-s', port, 'shell', 'getprop', 'sys.boot_completed'])
        check = check.decode().strip()
        if check == "1":
            print("completed")
            return 1
        time.sleep(2)
        i = i + 1
        print("wait" + str(i))
        # check = int(check)
        # return check


def check_running_avd():
    '''
        check if required avd in contextConfig in running avds
    '''
    list_avds = config.avd_file_reader()

    list_avds.pop(-1)

    emulator_instances = adb_instances_manager()

    running_emulator_model = []
    valid_model = []

    for instance in emulator_instances:
        running_emulator_model.append(instance.model)
    for avd in list_avds:
        if avd in running_emulator_model:
            pass
        else:
            valid_model.append(avd)
    print(valid_model)
    return valid_model


def emulator_runner(contexts: List):
    '''
    runs emulator based on the settings provided in context
    '''

    util.show_step(1)
    print(contexts['emulator_name'])
    if not is_context_avd_in_system_avds(contexts['emulator_name']):
        print('Error: provided context_avd ' +
              contexts['emulator_name'] + ' is not present in list of avds')
        print('Possible list of Avds are: ')
        util.detail_print(get_avd_list())
        return

    api_commands.adb_start_server_safe()
    util.show_step(4)

    avds = check_running_avd()

    if avds:
        emulator_port = get_running_avd_ports()
        if emulator_port:
            emulator_port = int(emulator_port[-1]) + 2
        else:
            emulator_port = 5555
    # print(emulator_port)
    #
    # The console port number must be an even integer between 5554 and 5584,
    # inclusive. <port>+1 must also be free and will be reserved for ADB.

    #
    # for name in avds:
    #     print(name)
    command = config.EMULATOR
    # command_argument = " -avd " + name
    #     print(command_argument)
    #     print(command + command_argument)
    subprocess.Popen([command,
                      '-port', str(emulator_port), '-avd',
                      context_list['emulator_name'], '-use-system-libs'],
                     stdout=subprocess.PIPE)
    # print(current_process.pid, emulator_port)
    check = check_avd_booted_completely(emulator_port)
    if check == 1:
        print(context_list['emulator_name'] + " has booted completely")
        flag = True
        return flag
    else:
        print(context_list['emulator_name'] + " has not booted completely")
        flag = False
        return flag
        #         emulator_port += 2
        #         emulator_processes.append(current_process)
        # else:
        #     print ("all AVD is allready running")


def get_name(uid):
    path = os.getcwd() + '/temp/' + uid + '/' + uid + '/context'
    with open(path, 'r') as f:
        first_line = f.readline()
    return first_line


def adb_instances_manager() -> List[Emulator]:
    '''
    returns the List of emulators.

    :returns `List[Emulator]`:

    '''
    emulators = []
    api_commands.adb_start_server_safe()
    adb_ports = api_commands.adb_list_avd_ports()
    for adb_port in adb_ports:
        pid = util.pid_from_emulator_port(adb_port)
        model = api_commands.avd_model_from_pid(pid)
        current_emulator = Emulator(adb_port, pid, model)
        emulators.append(current_emulator)
    util.detail_print(emulators)
    return emulators

def get_list_emulators():
    return adb_instances_manager()

def get_adb_instance_from_emulators(model: str) -> Emulator:
    '''
    returns the Emulator data type if specified model is matched.
    example:
        >>> get_adb_instances_from_emulators('Nexus6')
    '''
    emulators = adb_instances_manager()
    for emulator in emulators:
        if emulator.model == model:
            return emulator
    raise ValueError('No emulator found for ' + model)


def get_processid_of_adb_instance_by_model(emulators: List[Emulator], model: str):
    '''
    returns the PID of running adb_instance when the model name is specified
    '''
    if emulators and model:
        for emulator in emulators:
            if emulator.model == model:
                return emulator.pid
    else:
        return None


def get_device_emulator_model(output_raw):
    # print(output_raw)
    """
    PID TTY      STAT   TIME COMMAND
    15522 tty2     Rl+  128:13 /home/amit/Android/Sdk/tools/emulator64-x86 -port 5557 -avd nexus_s
    """
    current_string = output_raw.split('\n')[1:][:1][0]

    """
    15521 tty2     Rl+  134:48 /home/amit/Android/Sdk/tools/emulator64-x86 -port 5555 -avd nexus_4
    """
    index_of_avd = current_string.index('-avd')
    """
    nexus_s
    """
    return current_string[index_of_avd + 5:]


def is_context_avd_in_system_avds(context_avd: str) -> bool:
    '''
    returns boolean, if the provided `avd` name is in the list of System Avds
    '''

    if context_avd in get_avd_list():
        return True
    else:
        return False


def emulator_wipe_data(emulator: Emulator):
    '''
    wipes data for the specified emulator by `port`
    '''
    subprocess.check_output(
        [config.EMULATOR, '@' + emulator.model, '-wipe-data'])


def emulator_start_avd(port: int, emulator_name: str):
    subprocess.Popen([config.EMULATOR,
                      '-port', str(port), '-avd',
                      emulator_name, '-accel', 'auto', '-use-system-libs'],
                     stdout=subprocess.PIPE)


if __name__ == '__main__':
    # emulator_runner()
    adb_instances_manager()
