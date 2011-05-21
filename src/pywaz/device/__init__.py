class Device(object):
    """Base class of any inputdevices.
    This is the base class of Mouse, Key, Joypad.
    It provides users to unified api.
    This class is abstract.
    Device class instance can't create.
    """
    Mouse = 0
    Key = 1
    JoyPad = 2
    numbuttons = 0
    _type = None
    
    def __init__(self, id):
        raise NotImplementedError
    def is_press(self, key):
        return False
    def get_num_axes(self):
        return 0
    def get_axis(self, n):
        return 0
    def poll(self):
        pass
    def enable_repeat(self, key):
        pass
    def disable_repeat(self, key):
        pass
    def get_repeat(self, key):
        return False
    @property
    def type(self):
        return self._type
    def get_num_button(self):
        return self.numbuttons