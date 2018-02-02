from typing import Union


class XML_Element:
    '''This class contains element attributes'''

    def __init__(self, resource_id: str, element_class: str, checkable: str,
                 checked: str, clickable: str, enabled: str, focusable: str,
                 focused: str, scrollable: str, long_clickable: str,
                 password: str, selected: str, xpos: Union[float, int],
                 ypos: Union[float, int]) ->\
            None:
        self.resource_id = resource_id
        self.element_class = element_class
        self.checkable = checkable
        self.checked = checked
        self.clickable = clickable
        self.enabled = enabled
        self.focusable = focusable
        self.focused = focused
        self.scrollable = scrollable
        self.long_clickable = long_clickable
        self.password = password
        self.selected = selected
        self.xpos = xpos
        self.ypos = ypos

    def __str__(self) -> str:

        # return "[event_type: {}, step: {}, interval: {}, event: {}]".format(
        #     self.event_type, self.step, self.interval, self.event)
        return "{}".format(
            self.resource_id)

    __repr__ = __str__
