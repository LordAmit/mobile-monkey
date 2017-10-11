
#!/usr/bin/env python3

"""
util module
"""
from time import strftime, localtime
from typing import List
import enum
import os
import shutil
import subprocess


def show_step(step):
    """
    shows step
    """
    if True:
        print(step)


def check_file_directory_exists(address: str, to_quit: bool) -> bool:
    """
    checks if specified directory exists. if not, exits.
    :param address: address of file or directory to be checked.
    :param to_quit: determines if to exit if address does not exist.
    """
    if os.path.exists(address):
        return True
    else:
        print(address + " does not exist")
        if not to_quit:
            return False
        else:
            quit()


def move_dir_safe(source: str, destination: str):
    '''
        moves directory from `source` to `destination`
    '''

    if os.path.isdir(source) and os.path.isdir(destination):
        print('checked. Moving ', source, destination)
        remove_existing_file_directory(destination)
        shutil.move(source, destination)
    else:
        print('something wrong with safe_move: ')
        print(source, destination)

def StringToBoolean(value:str):
    if value == "True":
        return True
    elif value == "False":
        return False
    else:
        raise ValueError("value must be True/False. You provided: "+value)


def remove_existing_file_directory(address: str):
    """
    checks if the file/directory exists is provided address.
    if exists, removes. if not, nothing!
    :param address: address of file or directory
    """
    if check_file_directory_exists(address, False):
        try:
            shutil.rmtree(address)
        except NotADirectoryError:
            os.remove(address)


def kill_process_using_pid(pid: str):
    '''
        kills a process using specified `pid`
    '''
    if pid:
        try:
            subprocess.check_output(['kill', '-9', pid])
            print('killed process using pid: ' + pid)
        except subprocess.CalledProcessError:
            print('error. most possibly there is no pid by ' + pid)


def detail_print(variable):
    '''
    pretty prints the `variable`. If it is a `List`, it prints accordingly.
    '''
    import pprint
    if isinstance(variable, List):
        for i in variable:
            try:
                pprint.pprint(i.__dict__)
            except AttributeError:
                if isinstance(i, str):
                    print(i)

    else:
        pprint.pprint(variable.__dict__)


def list_as_enum_name_list(integer_list: List[int], enum_type) -> List[str]:
    '''
    replaces values based on names of enums
    '''
    if not integer_list:
        raise ValueError("List must not be empty")
    if not isinstance(enum_type, enum.EnumMeta):
        raise ValueError("enum_type must be enum")
    enum_name_list = []
    for i in integer_list:
        enum_name_list.append(enum_type(i).name)
    return enum_name_list


def return_current_time():
    '''
        returns current time in YYYYMMDDHHmm format.
    '''

    return strftime("%Y%m%d%H%M", localtime())


def return_current_time_in_logcat_style():
    '''
        return current time in logcat threadtime style
        "%m-%d %H::%M::%S"
    '''
    return strftime("%m-%d %H:%M:%S", localtime())


def debug_print(*msg: str, flag: bool):
    '''
    prints if the provided flag is true
    '''
    if flag:
        print(msg)


def pid_from_emulator_port(emulator_port: int) -> str:
    '''
        :param emulator_port:
            integer `emulator_port`

        returns:
            PID of provided `emulator_port`
    '''
    tcp_port = "tcp:" + str(emulator_port)
    # lsof -sTcp:LISTEN -iTcp:5555
    pid = subprocess.check_output(
        ['lsof', '-sTcp:LISTEN', '-i', tcp_port])
    pid = pid.decode()
    # COMMAND     PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
    # qemu-syst 11803 amit   52u  IPv4 1855210      0t0  TCP localhost:5555
    # (LISTEN)
    pid = pid.split('\n')[1:][0].split(' ')[1]
    # 11803
    return pid


def ps_details_of_pid(pid: str) -> str:
    '''
        retuns:
            device details from `pid`
    '''
    device_details = subprocess.check_output(['ps', str(pid)])
    device_details = device_details.decode().strip()
    return device_details


def change_file_permission(filename_with_full_path: str, permission: int):
    '''
        `permission` in 3 digit number
    '''

    check_file_directory_exists(filename_with_full_path, True)
    subprocess.check_output(
        ['chmod', str(permission), filename_with_full_path])


def print_dual_list(list_one: List, list_two: List):
    '''
    prints two same length lists matching  each other in the following format.
    eg:
    >>> "{}: {}".format(list_one[i], list_two[i])
    '''

    if not len(list_one) == len(list_two):
        raise ValueError("List length mismatched")
    for i in range(0, len(list_one) - 1):
        print("{}: {}".format(list_one[i], list_two[i]))
