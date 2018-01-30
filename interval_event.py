from typing import Union, Type, List

from adb_settings import UserRotation
from adb_settings import Airplane
from adb_settings import KeyEvent

from telnet_connector import TelnetAdb
from telnet_connector import GsmProfile
from telnet_connector import NetworkDelay
from telnet_connector import NetworkStatus
import util
import config_reader as config

EVENT_TYPES = Union[GsmProfile, NetworkDelay,
                    NetworkStatus, Airplane, UserRotation, KeyEvent]


class IntervalEvent:

    '''
    `Interval Event` class contains the steps,
    for each of which, an interval, an event and an event_type is assigned
    e.g.

    >>> [event_type: <enum 'NetworkStatus'>, step: 0, interval: 4, event: full]

    where `event_type` represents one of the Event Types:
    - GsmProfile,
    - NetworkDelay,
    - NetworkStatus,
    - Airplane,
    - UserRotation

    `step` is a 0 indexed list, against which an `interval` in seconds
    and an `event` of event_type is assigned.
    '''

    def __init__(self, step: int, interval: int, event: EVENT_TYPES, event_type: EVENT_TYPES)->None:
        self.step = step
        self.interval = interval
        self.event = event
        self.event_type = event_type

    def __str__(self) -> str:

        # return "[event_type: {}, step: {}, interval: {}, event: {}]".format(
        #     self.event_type, self.step, self.interval, self.event)
        return "{} {} {} {} {}".format(
            util.return_current_time_in_logcat_style(),
            self.event_type.__name__, self.step, self.interval, self.event)

    __repr__ = __str__


def read_interval_event_from_file(file_address: str,
                                  event_type: Type[EVENT_TYPES])->List[IntervalEvent]:
    '''
        imports event from file and returns `List[IntervalEvent]`
    '''
    util.check_file_directory_exists(file_address, True)
    lines: list = open(file_address).read().split('\n')
    step: int = 0
    event_type_name = None
    events: List[IntervalEvent] = []
    total_event_duration: int = 0
    for line in lines:
        in_values = line.split(',')
        if len(in_values) is 3:
            try:
                event_value = int(in_values[0])
                event_interval = int(in_values[1])
                event_type_name = str(in_values[2])
            except ValueError:
                print('Caught Error! Please check value of: ' + in_values)
            if in_values[2] == 'GsmProfile':
                i_event = IntervalEvent(
                    step, event_interval, GsmProfile(event_value).name, GsmProfile)
            elif in_values[2] == 'NetworkDelay':
                i_event = IntervalEvent(
                    step, event_interval, NetworkDelay(event_value).name, NetworkDelay)
            elif in_values[2] == 'NetworkStatus':
                i_event = IntervalEvent(
                    step, event_interval, NetworkStatus(event_value).name, NetworkStatus)
            elif in_values[2] == 'UserRotation':
                i_event = IntervalEvent(
                    step, event_interval, UserRotation(event_value).name, UserRotation)
            else:
                raise ValueError(
                    "incorrect format of Event type: " + in_values[2])
            events.append(i_event)
            total_event_duration += event_interval
            if total_event_duration > config.DURATION:
                print("total event interval duration from file (" +
                      str(total_event_duration)
                      + ") can not be larger than " + str(config.DURATION))
                raise ValueError()
    print("successfully imported from file. Type: " +
          event_type_name + "; total duration=" + str(total_event_duration))
    return events
