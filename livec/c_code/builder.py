

import c_types
import c_operators as c_ops
from c_expression import CodeBlock, Expression

class WrongNumberOfOperands(Exception): pass
class OperandTypeMismatch(Exception): pass

class CodeBuilder(object):
    def __init__(self):
        self.scope = None

    
    def build_expression(self, op, args):
        self.validate_types(op, args)
        return Expression(op, args)

    def validate_types(self, op, args):
        if op.allow_any_number_of_last_operand:
            compare_list = op.operand_types + [op.operand_types[-1]]*(len(args) - len(op.operand_types))
        else:
            if len(op.operand_types) != len(args):
                raise WrongNumberOfOperands(op, len(args), args)
            compare_list = op.operand_types


        for arg, allowed_type in zip(args, compare_list):
            if allowed_type == c_ops.SameAsRest:
                # just compare type to first one. all operands will have to be the same type anyway
                allowed_type = args[0].type

            if allowed_type == c_ops.OwnedField:
                if op == c_ops.AccessStructField:
                    if arg in self.get_type_of(args[0], None).fields:
                        continue
                    else:
                        raise OperandTypeMismatch('The field supplied for accessing the struct, is not a field of this struct type')
                else:
                    raise NotImplementedError()
                    
            arg_type = self.get_type_of(arg, allowed_type)

            if not arg_type == allowed_type:
                # TODO: shitty pythonic stuff. rid.
                try:
                    is_ok = isinstance(arg_type, allowed_type)
                except TypeError:
                    is_ok = False
                if not is_ok:
                    raise OperandTypeMismatch(op, "Arg is of type %r, expected %r" % (arg_type, allowed_type,))

    def get_type_of(self, arg, allowed_type):
        # TODO: REWRITE this whole crappy function.
        if isinstance(arg, Expression):
            if allowed_type == c_ops.BlockType:
                # any expression is valid here
                return allowed_type

            # TODO: We must find out what type this expression coerces to....
            if len(arg.op.result_types) == 0:
                # probably a problem...
                raise OperandTypeMismatch(op, "Arg is an expression with no result, "
                                          "can't be used in this operation that expects "
                                          "result of type %r" % (allowed_type,))
            else:
                result_type = arg.op.result_types[0]
                arg_type = result_type
                if result_type == c_ops.NumericalCoercion:
                    # TODO: coerce the args to a type
                    arg_type = self.numerical_coerce(arg.args)
                elif result_type == c_ops.LikeInternalType:
                    # TODO: deal with arrays, pointers, etc.
                    arg_type = self.get_type_of(arg.args[0], None).internal_type
                elif result_type == c_ops.OwnedFieldType:
                    if arg.op == c_ops.AccessStructField:
                        arg_type = arg.args[1].type # the type of the field being accessed in the struct
        else:
            arg_type = arg.type

        return arg_type
        
    def numerical_coerce(self, args):
        # TODO: put C's real coercion rules here
        # these are made-up rules.
        # REWRITE this whole crappy function.
        priority = ['long double',
                    'double',
                    'float',
                    'signed long',
                    'unsigned long',
                    'signed int',
                    'unsigned int',
                    'signed short',
                    'unsigned short',
                    'signed char',
                    'unsigned char']
        found = None
        for arg in args:
            arg_type = self.get_type_of(arg, None)
            name = arg_type.tname
            if isinstance(arg_type, c_ops.FixedNumericalType):
                name = arg_type.signed + ' ' + name
            if found is None:
                found = name
            else:
                if priority.index(found) > priority.index(name):
                    found = name
        if found in c_ops.fixed_types:
            return c_ops.fixed_types[found]
        return c_ops.float_types[found]
                
