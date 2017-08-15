from pathlib import Path
import shlex
import time
import util
from enum import Enum
import subprocess
import api_commands
import config_reader as config
from emulator import Emulator
from apk import Apk


class TestType(Enum):

    '''
    Test types to be used by the logcat
    '''
    Monkey = 0
    MobileMonkey = 1


class FatalWatcher():

    def __init__(self, log_file_path: str):
        self.log_file_path = log_file_path
        self.file_contents = None
        self.stop_watching = False

    def has_fatal_exception_watch(self):
        self.file_contents = Path(self.log_file_path).read_text()
        if "FATAL" in self.file_contents:
            return True
        return False

    def continuous_fatal_exception_watch(self):
        while self.has_fatal_exception_watch():
            if self.stop_watching is True:
                break
            time.sleep(3)
        return False


class Logcat:

    '''
        Class logcat. instantiated by `Emulator` and `Apk`
    '''

    def __init__(self, emulator: Emulator, apk: Apk, test_type: TestType):
        self.emulator = emulator
        self.apk = apk
        self.package_name = apk.package_name
        self.app_pid = None
        self.log_process = None
        self.test_type = test_type
        self.file_address = config.LOG_ADDRESS + \
            self.package_name + "_" + util.return_current_time() + \
            "_" + self.test_type.name + ".log"
        self.logfile = None

    def start_logcat(self):
        '''
        starts logcat of this instance.
        '''
        self.app_pid = api_commands.adb_pidof_app(self.emulator, self.apk)
        print("app_pid: " + self.app_pid)
        self.clear_logcat()
        command = "adb logcat --format=threadtime *:W --pid=" + self.app_pid
        self.logfile = open(self.file_address, 'w')
        self.log_process = subprocess.Popen(
            shlex.split(command), stdout=self.logfile)

    # def experimental_start_logcat(self, fuzz: Fuzzer):
    #     '''
    #     starts logcat of this instance.
    #     '''
    #     self.app_pid = api_commands.adb_pidof_app(self.emulator, self.apk)
    # print("app_pid: " + self.app_pid)
    #     print("experimental log")
    #     self.clear_logcat()
    #     command = "adb logcat --format=threadtime *:W --pid=" + self.app_pid
    #     self.logfile = open(self.file_address, 'w')
    #     self.log_process = subprocess.Popen(
    #         shlex.split(command), universal_newlines=True, stdout=subprocess.PIPE)
    #     while True:
    #         line = self.log_process.stdout.readline()
    #         self.logfile.write(line)
    #         if len(line) < 1:
    #             print("Fault")
    #             break
    #         print(line)
    #         if "FATAL" in line:
    #             fuzz.fatal_exception = True

        # self.log_process = subprocess.Popen(
        #     shlex.split(command), stdout=subprocess.PIPE)
        # while True:
        #     output = str(self.log_process.stdout.readline().decode())
        #     if output == '' and self.log_process.poll() is not None:
        #         self.logfile.close()
        #         self.log_process.kill()
        #         break
        #     if output:
        #         print(output.strip())
        #         self.logfile.write(output)
        #         if "FATAL" in output:
        #             print("fatal exception detected.")
        #             fuzz.fatal_exception = True
        #             self.logfile.close()
        #             self.log_process.kill()
                # self.logfile.flush()

    def stop_logcat(self):
        '''
        stops logcat of this instance and closes the file.
        '''
        self.logfile.close()
        self.log_process.kill()

    def clear_logcat(self):
        '''
        clears logcat
        '''
        command = "adb logcat --clear"
        subprocess.check_output(shlex.split(command))
