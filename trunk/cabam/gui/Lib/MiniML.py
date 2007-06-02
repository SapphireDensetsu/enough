
class TreeError(Exception): pass
class Tree(object):
    def __init__(self, value='', parent = None, tab_width=3):
        self.value = value
        self.parent = parent
        self.tab_width = tab_width
        self.children = []

    def __repr__(self):
        return '<%s value=%s, children=%r, parent=%r>' % (self.__class__.__name__,
                                                          self.value,
                                                          self.children,
                                                          self.parent)

    def load_from_file(self, filename):
        self.load(open(filename, 'rb'))
        
    def load(self, f):
        trees = []
        tree = self
        last_depth = -1
        
        for line_num, line in enumerate(f):
            for i,c in enumerate(line):
                if c != ' ':
                    break
            else:
                # empty line?
                pass
            depth = i

            if (depth % self.tab_width) != 0:
                raise TreeError(line_num, "tab width incorrect: %d" % (depth))

            depth /= self.tab_width
            if depth > last_depth:
                if depth - last_depth != 1:
                    raise TreeError(line_num, "depth is too deep (too many tabs between child and parent)")
            else:
                # find the parent
                while depth - 1 < last_depth:
                    tree = tree.parent
                    if tree is None:
                        raise TreeError(line_num, depth, last_depth, "Unexpected error (bug?)")
                    last_depth -= 1

            value = line[i:].rstrip()
            if value:
                new_tree = Tree(value)
                new_tree.tab_width = tree.tab_width
                new_tree.parent = tree
                tree.children.append(new_tree)
                tree = new_tree
                last_depth = depth
            else:
                pass

    def save_to_file(self, filename):
        self.save(open(filename, 'wb'))
        
    def save(self, file, depth=-1):
        if depth >= 0:
            # dont save root
            file.write(depth*' '*self.tab_width)
            file.write(self.value+'\n')
        for child in self.children:
            child.save(file, depth=depth+1)
        
    def find_child(self, value):
        for i, child in enumerate(self.children):
            if child.value == value:
                return i, child
        raise TreeError("No such child")
            
            
