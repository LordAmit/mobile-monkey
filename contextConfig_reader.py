'''
context config reader for app
'''
import configparser as ConfigParser
import config_reader as config


class ContextConfigReader(object):
    '''
    reads the context config
    '''

    def __init__(self):
        pass

    @staticmethod
    def context_config_reader(option, uid):
        '''
        reads the config file in the specified uid:
        :param option: specifies the option to look for
        :param uid: specifies the UID of the folder containing the contextConfigFile
        '''
        context_config = ConfigParser.ConfigParser()
        context_config_file_location = config.TEMP + uid + '/contextConfigFile'

        # context_config.read(
        #     "/home/amit/git/
        # mobile_application_contextual_testing/emulator_manager/temp/contextConfigFile")
        try:
            context_config.read(context_config_file_location)
            value = context_config.get('context', option)
            return value
        except ConfigParser.NoSectionError:
            print("Error: section context not found")
            exit()
        except FileNotFoundError:
            print(context_config_file_location + "  not found: ")
            exit()
