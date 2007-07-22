import sys
sys.path.append("..")

import c_code

from c_code.c_types import Field, FuncType, StructType, FunctionData, PointerType
from c_code.c_operators import Add, AssignValue, AccessStructField, FunctionReturn, SequentialExecution, DereferencePointer

from c_code.builder import CodeBuilder


c_int = c_code.c_types.fixed_types['signed int']

field1 = Field(c_int, 'moshe')
my_struct = StructType((field1,))

param1 = Field(PointerType(my_struct), 'param1')
my_func_t = FuncType(c_int, [param1])

local_i = c_int.make_instance(0)

builder = CodeBuilder()

c = builder.build_expression(SequentialExecution, [
    builder.build_expression(AssignValue, [local_i, builder.build_expression(AccessStructField, [builder.build_expression(DereferencePointer, [param1]), field1])]),
    builder.build_expression(AssignValue, [local_i, builder.build_expression(Add, [local_i, c_int.make_immediate(1)])]),
    builder.build_expression(FunctionReturn, [local_i]),
    ])

f_instance = my_func_t.make_instance(FunctionData(c, local_i))
