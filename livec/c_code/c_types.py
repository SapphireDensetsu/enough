'''Base definitions of Live C code model'''


# TODO: add const
# TODO: add checks (make sure the array entries instances are of correct type, etc...)
#       note - checks should be in the model (here) and not in the gui, because there could be many guis.
# TODO: add instance creation  checks (that when creating an int, the input is not float)
# TODO: Deal with scoping - should we have a "DefineInstance" operator?
# TODO: Deal with rvalues vs. lvalues
# TODO: Arrays' instances - we don't really want all those instances of all the entries to exist, what to do?

from base import CObject

class Type(CObject):
    type_class = 'generic'
    def __init__(self, name = None):
        self.meta = {}
        if name is not None:
            self.meta['name'] = name
    def make_instance(self, *args):
        raise NotImplementedError()
    def __repr__(self):
        return '<Type: type_class=%r, meta=%r>' % (self.type_class, self.meta,)
    
class TypeInstance(CObject):
    def __init__(self, _type, value, name=None):
        self.type = _type
        self.value = value
        self.meta = {}
        if name is not None:
            self.meta['name'] = name
    def __repr__(self):
        return '<%s: type=%r, value=%r, meta=%r>' % (self.__class__.__name__, self.type, self.value, self.meta)

class TypeImmediate(TypeInstance):
    pass
        
class NumericalType(Type):
    type_class='numerical'
    def __init__(self, tname, py_converter=None, name=None):
        super(NumericalType, self).__init__(name=name)
        self.py_converter = py_converter
        self.tname = tname
    def make_instance(self, py_value):
        return TypeInstance(self, self.py_converter(py_value))
    def make_immediate(self, py_value):
        return TypeImmediate(self, self.py_converter(py_value))

class FixedNumericalType(NumericalType):
    type_class='fixed numerical'
    def __init__(self, tname, signed, **kw):
        super(FixedNumericalType, self).__init__(tname, py_converter=long, name=name)
        self.signed = signed
    
fixed_types = {}
for tname in ['char', 'short', 'int', 'long', #'long long',
              ]:
    for signed in ('signed', 'unsigned'):
        name = signed+' '+tname
        fixed_types[name] = FixedNumericalType(tname, signed, name=name)

class FloatNumericalType(NumericalType):
    type_class='float numerical'
    def __init__(self, *args, **kw):
        kw['py_converter'] = float
        super(FloatNumericalType, self).__init__(*args, **kw)

float_types = {}
for tname in ['float', 'double', 'long double',
              ]:
    float_types[tname] = FloatNumericalType(tname, name=tname)

#-----------------------------------

class Field(object):
    def __init__(self, _type, name=None):
        self.type = _type
        self.meta = {}
        if name is not None:
            self.meta['name'] = name
    def __repr__(self):
        return '<Field: %r meta=%r>' % (self.type, self.meta)

class StructType(Type):
    type_class='struct'
    def __init__(self, fields, name=None):
        super(StructType, self).__init__(name=name)
        self.fields = fields
    def make_instance(self, field_instances):
        return TypeInstance(self, field_instances)

#----------------------------------

class FunctionData(object):
    def __init__(self, code_block, local_instances=[]):
        self.code_block = code_block
        self.local_instances = local_instances

class FuncType(Type):
    type_class='function'
    def __init__(self, ret_type, param_fields, name=None):
        super(FuncType, self).__init__(name=name)
        self.ret_type = ret_type
        self.param_fields = param_fields
    def make_instance(self, function_data):
        return TypeInstance(self, function_data)
    def type_repr(self):
        return '<FuncType: %r func(%r)>' % (self.ret_type, self.params)


#-----------------------------------
class ArrayType(Type):
    type_class='array'
    def __init__(self, entry_type, num_entries, name=None):
        super(ArrayType, self).__init__(name=name)
        self.num_entries = num_entries
        self.internal_type = entry_type
    def make_instance(self, entry_instances):
        return TypeInstance(self, entry_instances)
    
class PointerType(Type):
    type_class='pointer'
    def __init__(self, pointed_type, name=None):
        super(PointerType, self).__init__(name=name)
        self.internal_type = pointed_type
    def make_instance(self, pointed_address):
        return TypeInstance(self, pointed_address)

class InstancePointerType(PointerType):
    def make_instance(self, pointed_instance):
        return TypeInstance(self, pointed_instance)
    
#----------------------------------------------


