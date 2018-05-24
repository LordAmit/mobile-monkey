# MobiCoMonkey (beta)
(Previously known as mobile-monkey, we are still updating the readme file!)
MobiCoMonkey is a GUI based light-weight Android **Mo**bile app **Co**ntextual **Monkey** type stress testing tool.
It not only stress tests your application based on GUI events, but also contexts, such as

- Network Delay,
- Network Type,
- Network Speed,
- Key events (Alphanumeric, Volume, etc)
- Screen Orientation

## How it works
The steps of using Mobile-Monkey is fairly simple. Similar to the Monkey Stress Testing tool from Google, it requires only Android Application (APK) to function. In simple terms, the following takes place when you provide it an APK, along with a few parameters:

- It analyzes the permissions requested to guess the required contexts in the app.
- It then creates a set of contextual events at random intervals. You can also set the nature of the pseudo-random intervals by setting values in the `configFile`. A seed is used to control the pseudo random nature of the events generation.
- The system is flexible enough to `feed` a custom set of contextual events, but that part is not completely implemnented yet.
- It then loads up the emulator specified in the `configFile` and installs the app
- Using a combination of Android API and low level telnet connection, it sends those contextual events to the Emulator.

## Setup / Requirements / Dependencies

MobiCoMonkey was created and and tested in Linux Mint 18.3 and Ubuntu 16.04, 64 bit. It is dependent on:

- Android SDK
- Python 3.6

The `pip` requirements are kept in `requirements.txt` file. The installation steps are:

- Download/clone this repo
- activate a virtual environment consisting of python3.6
- execute `pip install -r requirements.txt`
- pip might throw errors, but those will probably be related to you getting offered a better version of pip dependencies. Please use `google.com`  to solve those.
- Check and modify the configFile as provided in the Config File Options section.

## Config File Options
Mobile Monkey is dependent on `configFile`. It is also configurable using the same file. The following options are available:

### Dependencies

| Key               | Meaning                                                                                                                                                 |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| root              | the root directory                                                                                                                                      |
| directory         | directory where apk files of apps are kept                                                                                                              |
| adb               | path of adb from Android SDK                                                                                                                            |
| aapt              | path of aapt from Android SDK                                                                                                                           |
| emulator          | path of emulator from Android SDK                                                                                                                       |
| android           | path of android from Android SDK                                                                                                                        |
| tools             | path of tools from Android SDK                                                                                                                          |
| current_directory | path of the current directory of mobile-manager                                                                                                         |
| temp              | path of the temporary directory, where the apk files are extracted and analyzed                                                                         |
| telnet_key        | value of the telnet key. Generally found in a file called `.emulator_console_auth_token` from your home directory. Automatically created by Android SDK |
| localhost         | is required for telnet                                                                                                                                  |
| apktool           | tool required for testing unsigned apks or 3rd party apks. can be collected from [here](https://ibotpeaches.github.io/Apktool/install/).                |

### Configurations

Mobile-Monkey is configurable in various ways using the `configFile`. All duration keys specified below are in seconds unless otherwise specified.

| Key              | Value                                                                                                                                                                                |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| minimum_interval | minimum interval between contextual events                                                                                                                                           |
| maximum_interval | maximum interval between contextual events. Must be greater than minimum_interval and less than duration                                                                             |
| monkey_interval  | Mobile-Monkey can utilize the `monkey` tool from Google internally. monkey_interval is the interval between each events from monkey in millilseconds                                 |
| headless         | Determines whether the emulator will run in headless mode or not, only accepts `True/False`                                                                                          |
| seed             | seed is used to control the Pseudo-randomness of interval_events. integers only                                                                                                      |
| duration         | the complete duration of contextual stress testing                                                                                                                                   |
| apk_name         | name of the apk file without the apk extension                                                                                                                                       |
| apk_full_path    | the full path is automatically deduced by combining the `root` and `apk_name`. You need to provide the rest of the path                                                              |
| emulator_name    | Case Sensitive name of the emulator to be used. Must be created before using.                                                                                                        |
| emulator_port    | mobile_monkey will try to start the emulator using this port. 5555 is the default, however it may sometimes change due to unavailability of the port. Mobile-Monkey can handle that. |
| log_address      | path where logs will be kept                                                                                                                                                         |
| dump_address     | path where uiautomator dumps will be kept                                                                                                                                            |


### Others

The following key values are created for debugging purposes.
 - log_file
 - sample_log
 - monkey_log_file
 - mobile_monkey_log_file
 - mobile_monkey_log

These will be removed at later stages in the stable release.

## Running Mobile-Monkey
We are assuming that you have setup the `configFile` properly and have your APK prepared. At all times,we are also assuming that you are in a python3.6 virtual environment. Now, from the mobile-monkey directory:

- `python install_app.py` will start the emulator and install the app
- you now have two options. you can either run `monkey` from Google through mobile-monkey, or you can run `mobile-monkey`.
    To run mobile-monkey, type:

    ```python mobile_monkey.py```

    after successful execution, mobile-monkey will create a log file of execution in `apkname_YYYYMMDDHHMM_MobileMonkey.log` format.

    to run monkey, type:

    ```python run_monkey_only.py```

    after successful execution, mobile-monkey will create a log file of execution in `apkname_YYYYMMDDHHMM_Monkey.log` format.
- in both cases, mobile_monkey will stop contextual events execution in case a fatality or error occurs during execution.
- It will also display in terminal what contextual event it is executing. A different option will be provided later that will help it store the contextual events sequence for checking.
- Finally, it will show you a list containing number  of errors, warnings, unique errors, and unique warnings the app created during execution.

Please note that we have tried our best to clean up the warnings and errors related to advertisement, but everyone uses different formats of advertisement integration. Therefore, it is highly advised to remove your advertisement integration before testing the app.