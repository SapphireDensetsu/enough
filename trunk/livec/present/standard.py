import sys
sys.path.append("..")

import c_code

from c_code import c_operators as c_ops
from c_code import c_types
from present.base import CodePresenter


class StandardPresenter(CodePresenter):
    def __init__(self):
        self.name_count = 0
        self.ex_presenters = {c_ops.Multiply: self.present_twosided_op,
                              c_ops.Add: self.present_twosided_op,
                              c_ops.Divide: self.present_twosided_op,
                              c_ops.Subtract: self.present_twosided_op,
                              c_ops.Remainder: self.present_twosided_op,
                              c_ops.IsEqual: self.present_twosided_op,
                              c_ops.AssignValue: self.present_twosided_op,
                              c_ops.AccessStructField: self.present_twosided_op,
                              
                              
                              c_ops.SequentialExecution: self.present_sequential,
                              
                              c_ops.FunctionReturn: self.present_unary_pre,
                              c_ops.DereferencePointer: self.present_unary_pre,

                              }
        
        self.declare_presenters = {c_types.NumericalType: self.declare_num,
                                   c_types.FuncType: self.declare_func,
                                   c_types.StructType: self.declare_struct,
                                   c_types.ArrayType: self.declare_array,
                                   c_types.PointerType: self.declare_pointer,
                                   }
            
##         self.define_presenters = (c_types.NumericalType: self.define_num,
##                                   c_types.FuncType: self.define_func,
##                                   c_types.StructType: self.define_struct,
##                                   c_types.ArrayType: self.define_array,
##                                   c_types.PointerType: self.define_pointer,
##                                   )

    def write(self, st):
        sys.stdout.write(st)
        
    def present_expression(self, exp):
        if isinstance(exp, c_types.TypeInstance):
            self.write(self.generate_name(exp))
            return
        if isinstance(exp, c_types.Field):
            self.write(self.generate_name(exp))
            return
        self.ex_presenters[exp.op](exp)

    def present_sequential(self, exp):
        for arg in exp.args:
            self.present_expression(arg)
            self.write(';\n')

    def _generate_new_name(self, cobj):
        name = 'obj__' + str(self.name_count)
        self.name_count += 1
        cobj.meta['name'] = name
        return name
        
    def generate_name(self, cobj):
        if 'name' in cobj.meta:
            return cobj.meta['name']
        if isinstance(cobj, c_types.TypeInstance):
            return self._generate_new_name(cobj)

        # ITs a type
        if isinstance(cobj, c_types.NumericalType):
            name = cobj.tname
            if isinstance(cobj, c_types.FixedNumericalType):
                name = cobj.signed + ' ' + name
            return name

        if isinstance(cobj, c_types.StructType):
            name = 'struct ' + self._generate_new_name(cobj)
            cobj.meta['name'] = name
            return name

        raise NotImplementedError(cobj)


    def present_declaration(self, cobj):
        # TODO: But can you declare structs, or do define structs? structs are types, too....
        if not isinstance(cobj, c_types.TypeInstance) and not isinstance(cobj, c_types.Field):
            # TODO: Implement typedefs here and elsewhere
            raise TypeError("You can only declare instances or fields (or typedefs in the future), but not types (arg was %r)." % (cobj,))

        if cobj.type in self.declare_presenters:
            key = cobj.type
        else:
            # The instance's type may be a subclass
            for key in self.declare_presenters:
                if isinstance(cobj.type, key):
                    break
            else:
                raise ValueError("No implementation exists for instances of %r" % (cobj.type,))
            
        self.declare_presenters[key](cobj)
        
##     def present_definition(self, cobj):
##         # TODO this is COPY PASTE from present declaration. DOH!
##         if not isinstance(cobj, c_types.TypeInstance) and not isinstance(cobj, c_types.Field):
##             # TODO: Implement typedefs here and elsewhere
##             raise TypeError("You can only declare instances or fields (or typedefs in the future), but not types (arg was %r)." % (cobj,))

##         if cobj.type in self.declare_presenters:
##             key = cobj.type
##         else:
##             # The instance's type may be a subclass
##             for key in self.declare_presenters:
##                 if isinstance(cobj.type, key):
##                     break
##             else:
##                 raise ValueError("No implementation exists for instances of %r" % (cobj.type,))
            
##         self.define_presenters[key](cobj)
        
        
    
    def present_twosided_op(self, exp):
        op_name_map = {c_ops.Multiply: ' * ',
                       c_ops.Add: ' + ',
                       c_ops.Divide: ' / ',
                       c_ops.Subtract: ' - ',
                       c_ops.Remainder: ' % ',
                       c_ops.IsEqual: ' == ',
                       c_ops.AssignValue: ' = ',
                       c_ops.AccessStructField: '.',
                       c_ops.AccessArrayElement: '[',
                       }
        self.present_expression(exp.args[0])
        self.write(op_name_map[exp.op])
        self.present_expression(exp.args[1])
        
        if exp.op == c_ops.AccessArrayElement:
            self.write(']')

    def present_unary_pre(self, exp):
        op_name_map = {c_ops.FunctionReturn: 'return ',
                       c_ops.DereferencePointer: '*',
                       c_ops.AddressOf: '&',
                       }
        self.write(op_name_map[exp.op])
        if len(exp.args) > 0:
            self.present_expression(exp.args[0])
        
    def declare_num(self, num_instance):
        self.write(self.generate_name(num_instance.type) + ' ' + self.generate_name(num_instance))
    
    def declare_pointer(self, pointer_instance):
        self.write(self.generate_name(pointer_instance.type.internal_type) + ' *' +
                   self.generate_name(pointer_instance))

    def declare_array(self, instance):
        self.write(self.generate_name(instance.type.internal_type) + ' ' +
                   self.generate_name(instance) + '[%d]' % (instance.type.num_entries,))

    def declare_func(self, instance):
        self.write(self.generate_name(instance.type.ret_type) + ' ' +
                   self.generate_name(instance) + '(')
        for param_field in instance.type.param_fields:
            self.present_declaration(param_field)
        self.write(')')

    def declare_struct(self, instance):
        self.write(self.generate_name(instance.type) + ' ' + self.generate_name(instance))
        for field in instance.type.fields:
            self.present_declaration(field)
            self.write(';\n')
        self.write('}')
        


# TODO: Place default values
##     def define_num(self, num_instance):
##         self.write(self.generate_name(num_instance.type) + ' ' + self.generate_name(num_instance))
    
##     def define_pointer(self, pointer_instance):
##         self.write(self.generate_name(pointer_instance.type.internal_type) + ' *' +
##                    self.generate_name(pointer_instance))

##     def define_array(self, instance):
##         self.write(self.generate_name(instance.type.internal_type) + ' ' +
##                    self.generate_name(instance) + '[%d]' % (instance.type.num_entries,))

##     def define_func(self, instance):
##         self.write(self.generate_name(instance.type.ret_type) + ' ' +
##                    self.generate_name(instance) + '(')
##         for param_field in instance.type.param_fields:
##             self.present_declaration(param_field)
##         self.write(')')

##     def define_struct(self, instance):
##         self.write(self.generate_name(instance.type) + ' ' + self.generate_name(instance) + '{')
##         for field in instance.type.fields:
##             self.present_definition(field)
