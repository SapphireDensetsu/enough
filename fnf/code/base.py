from WeakCollection import WeakCollection
from DisjointSets import DisjointSets
from Event import Event

from functools import partial

class Field(object):
    def __init__(self, cls, meta=None):
        self.cls = cls
        if meta is None:
            meta = {}
        self.meta = meta

    def __repr__(self):
        return '<%s, cls=%r, meta=%r>' % (self.__class__.__name__, self.cls, self.meta)
    
class Instance(object):
    def __init__(self, cls, meta=None):
        self.cls = cls
        if meta is None:
            meta = {}
        self.meta = meta
        # This is a map from field to instance of that field
        self._fields_instances = {}
        self.event_modified = Event()
        self.event_field_instance_set = Event()
        self.event_field_instance_removed = Event()
        self.event_field_instance_linked = Event()
        
        for field in cls.fields:
            if field not in self._fields_instances:
                field_instance = self.create_field_instance(field)
                self.set_field_instance(field, field_instance)
                self.event_field_instance_set.send(self, field, field_instance)
                
        # TODO send this event somewhere when a new value propogates through us
        #self.event_modification_propogating = Event()

    def create_field_instance(self, field):
        field_instance = field.cls.create_instance()
        return field_instance

    def set_field_instance(self, field, field_instance):
        if field in self._fields_instances:
            assert 0, "trying to set same field twice!"
        self._fields_instances[field] = field_instance
        #self.subfield_linked((field,), field_instance)
        field_instance.event_modified.register(partial(self.field_modified, self, field_instance), key=(self, field))

        # This should be called externally?
        self.event_field_instance_set.send(self, field, field_instance)
        
        return field_instance

    def remove_field_instance(self, field_instance):
        field = self.field_of_field_instance(field_instance)
        field_instance.event_modified.unregister((self, field))
        del self._fields_instances[field]
        # this should be called externally?
        self.event_field_instance_removed.send(self, field, field_instance)

        
##     def copy(self):
##         new = self.cls.create_instance()
##         new.meta.update(self.meta)
##         return new
    
    def __repr__(self):
        return '<%s at 0x%X, cls=%r, meta=%r>' % (self.__class__.__name__, id(self), self.cls, self.meta)

    # todo is this normal?!
    @staticmethod
    def field_modified(self, field_instance, modified_instance, modified_by):
        #print 'field modified', self, field_instance, modified_instance, modified_by
        if modified_by is self:
            return
        self.event_modified.send(field_instance, modified_by)
        
    def get_subfield_instance(self, subfield_hierarchy, stop_at_parent):
        # Returns the requested subfield's parent, the requested subfield (parent, subfield)
        if stop_at_parent:
            if len(subfield_hierarchy) == 1:
                return self
            subfield_hierarchy = subfield_hierarchy[:-1]
        subfield_instance = self
        # Deeply go into children, grandchildren, etc. until we reach the actualy instance involved
        for subfield in subfield_hierarchy:
            subfield_instance = subfield_instance._fields_instances[subfield]
        return subfield_instance

    def replace_field_instance(self, field, new_instance, modified_by):
        # This is called when a new instance is placed for afield
        if field not in self.cls.fields:
            raise ValueError("Unknown field", field, self.cls.fields)
        old_instance = self._fields_instances[field]

        if old_instance != new_instance:
            self.remove_field_instance(old_instance)
            self.set_field_instance(field, new_instance)
        
        # In this case we must send a 'modified' event because some magic function
        # might need to re-calculate because one of it's fields has changed it's instance
        self.event_modified.send(new_instance, modified_by)
        
        return new_instance

    def link_field_instance(self, field, new_instance, modified_by):
        old_instance = self._fields_instances[field]
        self.event_field_instance_linked.send(self, old_instance, new_instance)
        self.replace_field_instance(field, new_instance, modified_by)
        
    # a subfield_hierarchy is a list of: field_A, subfield_B, subsubfield_C, etc...
    def subfield_linked(self, src_subfield_hierarchy, src_subfield_instance):
        #print 'src len', self, len(src_subfield_hierarchy)
        # Replaces the instances of all subfields using the given one
        linked_subfields_hierarchies = self.cls.links.set_of(src_subfield_hierarchy)
        #print 'number of links', len(linked_subfields_hierarchies)
        for subfield_hierarchy in linked_subfields_hierarchies:
            subfield_parent_instance = self.get_subfield_instance(subfield_hierarchy, True)
            
            subfield_parent_instance.link_field_instance(subfield_hierarchy[-1], src_subfield_instance, self)

    def subfield_unlinked(self, subfield_hierarchy):
        # in this case we can go straight to the depest level, and insert a new instance
        # TODO copy the instance instead of just creating new
        subfield_parent_instance = self.get_subfield_instance(subfield_hierarchy, True)
        
        old_subfield_instance = subfield_parent_instance._fields_instances[subfield_hierarchy[-1]]
        new_subfield_instance = subfield_parent_instance.create_field_instance(subfield_hierarchy[-1])
        # old_subfield_instance.copy() #subfield_hierarchy[-1].cls.create_instance()

        subfield_parent_instance.replace_field_instance(subfield_hierarchy[-1], new_subfield_instance, self)
        


    # UTility functions
    def subfield_hierarchy_by_instance(self, subfield_instance, return_empty_list_if_none=False):
        for field, field_instance in self._fields_instances.iteritems():
            res = [field]
            if subfield_instance is field_instance:
                return res
            f_res = field_instance.subfield_hierarchy_by_instance(subfield_instance, return_empty_list_if_none=True)
            if f_res:
                res.extend(f_res)
                return res
        if return_empty_list_if_none:
            return []
        # This can happen if someone stupid requested the hierarchy to an instance that is not our subfield!
        raise ValueError("No such subfield instance", subfield_instance)

    def field_of_field_instance(self, field_instance):
        for field, fi in self._fields_instances.iteritems():
            if fi == field_instance:
                return field
        raise ValueError("No such field instance")
        
    def field_instances(self):
        return list(self._fields_instances.values())
    
    def field_instances_by_name(self):
        # Utility func
        res = {}
        for field, field_instance in self._fields_instances.iteritems():
            res[field.meta['name']] = field_instance
        return res
    def fields_by_name(self):
        # Utility func
        res = {}
        for field, field_instance in self._fields_instances.iteritems():
            res[field.meta['name']] = field
        return res
    def self_modified(self, modified_by):
        # todo if instances are immutable, this shouldn't exist!
        self.event_modified.send(self, modified_by)
    
    
class Class(object):
    def __init__(self, meta=None, fields=tuple()):
        if meta is None:
            meta = {}
        self.meta = meta
        self.fields = list(fields)
        self.instances = WeakCollection()
        # Each set of linked subfields means that those subfields are linked and share the same instance
        self.links = DisjointSets()
        
    def __repr__(self):
        return '<%s, meta=%r, fields=%r>' % (self.__class__.__name__, self.meta, len(self.fields))

    def create_instance(self, **kw):
        instance = Instance(self, **kw)
        self.instances.add(instance)
        return instance

    def union(self, src_subfield_hierarchy, dst_subfield_hierarchy):
        src_subfield_hierarchy = tuple(src_subfield_hierarchy)
        dst_subfield_hierarchy = tuple(dst_subfield_hierarchy)
        self.links.union(src_subfield_hierarchy, dst_subfield_hierarchy)
        assert dst_subfield_hierarchy in self.links.set_of(src_subfield_hierarchy)
        assert src_subfield_hierarchy in self.links.set_of(dst_subfield_hierarchy)
        
        for instance in self.instances:
            # Find the subfield's_instance for this instance (extract the instance from the deepest level)
            src_subfield_instance = instance.get_subfield_instance(src_subfield_hierarchy, False)
            
            # Tell the instance that the subfield has changed, it will update all internally linked fields to point
            # to the new instance.
            instance.subfield_linked(src_subfield_hierarchy, src_subfield_instance)

    def split(self, subfield_hierarchy):
        self.links.split(subfield_hierarchy)
        for instance in self.instances:
            instance.subfield_unlinked(subfield_hierarchy)


        
class MagicClass(Class):
    def __init__(self, *args, **kw):
        super(MagicClass, self).__init__(*args, **kw)
        self.event_instance_init = Event()
        self.event_instance_modified = Event()
        
    # A Basic, built-in, datatype
    def create_instance(self, **kw):
        instance = super(MagicClass, self).create_instance(**kw)
        instance.event_modified.register(partial(self.instance_modified, instance), key=self)
        self.event_instance_init.send(instance)
        return instance

    def instance_modified(self, *args):
        self.event_instance_modified.send(*args)


def make_magic_class(cls):
    c = MagicClass(meta=cls.meta, fields=cls.fields)
    c.__name__ = cls.__name__
    c.event_instance_init.register(cls.init, key=cls)
    c.event_instance_modified.register(cls.modified, key=cls)
    return c

def make_magic_value_class(name, default_value, **kw):
    c = MagicClass(**kw)
    c.__name__ = name
    def init(instance):
        if 'value' not in instance.meta:
            instance.meta['value'] = default_value
    c.event_instance_init.register(init)
    return c
