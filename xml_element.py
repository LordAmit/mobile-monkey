class XML_Element:
    '''This class contains element attributes'''

    def __init__(self, resource_id: str, element_class: str, checkable: str, checked: str, 
                 clickable: str, enabled: str, focusable: str, focused: str, scrollable:str,
                 long_clickable:str, password:str, selected:str, xpos:int, ypos: int):
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
