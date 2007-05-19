from __future__ import division
from base import make_magic_class, Field, MagicClass, make_magic_value_class


fnf_number = make_magic_value_class('fnf_number', 0, meta={'name': 'number'})
fnf_bool = make_magic_value_class('fnf_bool', False, meta={'name': 'bool'})

binary_number_fields = (Field(fnf_number, dict(name='a')), Field(fnf_number, dict(name='b')), Field(fnf_number, dict(name='r')))

def fnf_number_of(num):
    return fnf_number.create_instance(meta=dict(value=num))

def simple_binary_op_maker(name):
    def simple_binary_op(pyfunc):
        class _temp(object):
            meta = {'name': name}
            fields = binary_number_fields
            @staticmethod
            def init(self):
                pass

            @staticmethod
            def modified(self, field, self_modified):
                if self_modified:
                    return
                #assert field in self.cls.fields, "unknown field modified in magic class"
                mod_instance = self.get_subfield_instance((field,), False)
                fields_by_name = self.fields_by_name()
                f = self.field_instances_by_name()
                a,b,r = f['a'], f['b'], f['r']

                if mod_instance in (a,b):
                    r_res = pyfunc(a.meta['value'], b.meta['value'], None)
                    self.modify_field_by_name('r', fnf_number_of(r_res), True)
                else:
                    b_res = pyfunc(a.meta['value'], None, r.meta['value'])
                    self.modify_field_by_name('b', fnf_number_of(b_res), True)
        return make_magic_class(_temp)
    return simple_binary_op


@simple_binary_op_maker('+')
def add(a, b, r):
    if r is None and None not in (a,b):
        return a+b
    elif b is None and None not in (r,a):
        return r-a
    elif a is None and None not in (r,b):
        return r-b
    else:
        assert 0, "Unknown params"
        

@simple_binary_op_maker('*')
def mul(a, b, r):
    if r is None and None not in (a,b):
        return a*b
    elif b is None and None not in (r,a):
        return r/a
    elif a is None and None not in (r,b):
        return r/b
    else:
        assert 0, "Unknown params"
        


if __name__=='__main__':
    try:
        a = add.create_instance()
        a.modify_field(a.fields_by_name()['a'], fnf_number.create_instance(meta={'value': 1}))
        a.modify_field(a.fields_by_name()['b'], fnf_number.create_instance(meta={'value': 3}))
    except:
        import pdb
        #pdb.pm()
        raise
