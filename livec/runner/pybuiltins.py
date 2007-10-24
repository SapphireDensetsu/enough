

class PyType(object):
    last_address = [0]
    address = 0

    def __init__(self, size):
        self.address = self.AllocateAddress(size)
        self.size = size
        
    @staticmethod
    def AllocateAddress(size):
        addr = last_address[0]
        last_address[0] += size
        return addr
    
    def AddressOf(self):
        return self.address

class RangeError(Exception): pass

class RangeCheckedType(PyType):
    def __init__(self, size, _min, _max):
        PyVariable.__init__(self, size)
        self.min = _min
        self.max = _max
        
    def check(self, value):
        if value < self.min or value > self.max:
            raise RangeError(self, self.value)

class RangeChecked
    def get_value(self):
        return self._value
    def set_value(self, nvalue):
        self.check(nvalue)
        self._value = nvalue
    value = property(get_value, set_value)

def bitsized_int(bits, signed):
    assert bits % 8 == 0
    half_range = 2**(bits-1)
    if signed:
        _min = -half_range
        _max = half_range-1
    else:
        _min = 0
        _max = 2*half_range
    return RangeCheckedType(bits/8, _min=_min, _max=_max)

PyInt = bitsized_int(32, True)
PyUnsignedInt = bitsized_int(32, False)
PyChar = bitsized_int(8, True)
PyUnsignedChar = bitsized_int(8, False)

class OutOfBoundsError(Exception): pass

class PyArray(PyVariable):
    def __init__(self, elem_type, num_elems):
        PyVariable.__init__(self, elem_type.size)
        self.elem_type = elem_type
        self.num_elems = num_elems
        self.elems = None

    def init_elems(self):
        if self.elems is None:
            self.elems = [elem_type.get_default_value() for i in xrange(num_elems)]

    def check_index(self, index):
        if index > self.num_elems or index < 0:
            raise OutOfBoundsError(self, index)
    
    def set_elem(self, index, value):
        self.init_elems()
        self.check_index(index)
        self.elems[index] = value
    def get_elem(self, index):
        self.init_elems()
        self.check_index(index)
        return self.elems[index]
    
