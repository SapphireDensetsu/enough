# Copyright (c) 2007 Enough Project.
# See LICENSE for details.

## /* Copyright 2007, Eyal Lotem, Noam Lewis, enoughmail@googlegroups.com */
## /*
##     This file is part of Enough.

##     Enough is free software; you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation; either version 3 of the License, or
##     (at your option) any later version.

##     Enough is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.

##     You should have received a copy of the GNU General Public License
##     along with this program.  If not, see <http://www.gnu.org/licenses/>.
## */

class UnallowedField(Exception): pass
class DuplicateFields(Exception): pass
class MissingField(Exception): pass
class UnexpectedFields(Exception): pass

class AttrDict(object):
    allowed_fields = [] # all allowed
    def __init__(self, *args, **kw):
        given_fields = kw.keys()
        if len(set(given_fields)) != len(given_fields):
            raise DuplicateFields(given_fields)

        given_args = list(args)
        for field in self.allowed_fields:
            if (len(field) == 1):
                field_name, = field
                mandatory = True
            else:
                try:
                    field_name, default = field
                except ValueError:
                    print 'Error with field:', repr(field)
                    raise
                mandatory = False

            if given_args:
                value = given_args.pop(0)
                if field_name in kw:
                    raise DuplicateFields(field_name, 'is already in args list')
            else:
                if field_name not in kw:
                    if mandatory:
                        raise MissingField(field_name)
                    else:
                        value = default
                else:
                    given_fields.remove(field_name)
                    value = kw[field_name]
            setattr(self, field_name, value)
        if given_fields:
            raise UnexpectedFields(given_fields)
    def __repr__(self):
        return '<%s at %r: %s>' % (self.__class__.__name__, id(self), ' '.join(('%s=%s' % (field[0],getattr(self, field[0]))) for field in self.allowed_fields))
    
    def shallow_copy(self):
        args = []
        for field in self.allowed_fields:
            field_name = field[0]
            args.append(getattr(self, field_name))
        return type(self)(*args)

