import util
from typing import List
import subprocess
import config_reader as config


class Apk:

    '''
    Apk class that contains apk_path, apk_name, and apk_permissions
    '''

    def __init__(self, apk_path: str)-> None:
        util.check_file_directory_exists(apk_path, True)
        self.apk_path = apk_path
        self.package_name = self.__adb_package_name_from_apk(apk_path)
        self.permissions = self.__adb_permissions_from_apk(apk_path)

    def __adb_package_name_from_apk(self, apk_path):
        '''
        returns the package_name by executing
            >>> aapt d permissions file.apk
        '''
        # ./aapt d permissions ~/git/testApps/Ringdroid_2.7.4_apk-dl.com.apk
        util.check_file_directory_exists(apk_path, True)
        result = subprocess.check_output(
            [config.AAPT, 'd', 'permissions', apk_path]).decode()
        return result.split("\n")[0].split('package:')[1].strip()

    def __adb_permissions_from_apk(self, apk_path: str):
        '''
        returns list of permissions defined in APK
        '''
        def extract_permission(value: str):
            '''
            internal function
            '''
            if ".permission." in value:
                if value.endswith('\''):
                    permission = value.split("=")[1].strip('\'')
                else:
                    permission = value.split(": ")[1]
                return permission

        util.check_file_directory_exists(apk_path, True)

        output = subprocess.check_output(
            [config.AAPT, 'd', 'permissions', apk_path]).decode().split('\n')
        result = list(filter(None, map(extract_permission, output)))
        return result

    def __str__(self):
        return "path: {}, package: {}, permissions: {}".format(
            self.apk_path, self.package_name, self.permissions
        )
