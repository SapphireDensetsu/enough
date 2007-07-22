import sys
sys.path.append('..')

from c_code.base import CObject

from c_types import Type, NumericalType, PointerType, StructType, ArrayType, FixedNumericalType, fixed_types


class Operator(CObject):
    def __init__(self, operand_types, result_types,
                 allow_any_number_of_last_operand=False,
                 name=None):
        self.operand_types = operand_types
        if SameAsRest in self.operand_types:
            same_op_type = None
            for t in self.operand_types:
                if t != SameAsRest:
                    if same_op_type is not None:
                        same_op_type = t
                    else:
                        raise ValueError("Inconsistent usage of SameAsRest. Only one type can be forced.")
        
        self.allow_any_number_of_last_operand = allow_any_number_of_last_operand
        if allow_any_number_of_last_operand:
            if len(operand_types) == 0:
                raise ValueError('For allow_any_number_of_last_operand=True, you MUST supply at least one operand type')

        if len(result_types) > 1:
            raise ValueError("Currently only 0 or 1 result types are allowed.")
        self.result_types = result_types
        
        self.meta = {}
        if name:
            self.meta['name'] = name
            
    def __repr__(self):
        num = len(self.operand_types)
        if self.allow_any_number_of_last_operand:
            num = 'AnyNumber'
        return '<%s: %s-ary, %r, meta=%r>' % (self.__class__.__name__, num, self.operand_types, self.meta)


#------------------------------------------------------------------------------

class SameAsRest(object): pass
class BlockType(object): pass

class AnyNumberOfOperands(object): pass

class NumericalCoercion(object): pass
class LikeInternalType(object): pass

class OwnedField(object): pass
class OwnedFieldType(object): pass

#------------------------------------------------------------------------------


Multiply = Operator([NumericalType, NumericalType], [NumericalCoercion], name='Multiply')
Add = Operator([NumericalType, NumericalType], [NumericalCoercion], name='Add')
Divide = Operator([NumericalType, NumericalType], [NumericalCoercion], name='Divide')
Subtract = Operator([NumericalType, NumericalType], [NumericalCoercion], name='Subtract')
Remainder = Operator([NumericalType, NumericalType], [NumericalCoercion], name='Remainder')
IsEqual = Operator([NumericalType, NumericalType], [NumericalCoercion], name='IsEqual')

#------------------------------------------
# what restrictions are on the things you can assign?
AssignValue = Operator([SameAsRest, SameAsRest], [SameAsRest], name='AssignValue')

#------------------------------------------

# opearnds: pointer
DereferencePointer = Operator([PointerType], [LikeInternalType], name='DereferencePointer')

# operands: array, index
AccessArrayElement = Operator([ArrayType, FixedNumericalType], [LikeInternalType], name='AccessArrayElement')

# operand: instance
AddressOf = Operator([SameAsRest], [fixed_types['signed long']], name='AddressOf')

# operands: struct instance, field
AccessStructField = Operator([StructType, OwnedField], [OwnedFieldType], name='AccessStructField')

#------------------------------------------

FunctionReturn = Operator([SameAsRest], [], name='FunctionReturn')

# TODO: Does a code block have a result type? Or while and if?
SequentialExecution = Operator([BlockType], [], allow_any_number_of_last_operand=True, name='SequentialExecution')

Break = Operator([], [], name='Break')
Continue = Operator([], [], name='Continue')
    
# operands are: condition expression, repeating expression (or code block)
While = Operator([NumericalType, BlockType], [], name='While')

# operands: condition expression, expression  if true, expression if false
IfElse = Operator([NumericalType, BlockType, BlockType], [], name='IfElse')

    
