class TypeManager:
    def __init__(self):
        self.types = {}

    def _add_default_types(self):
        for type in default_types:
            self.add_type(type)

    def add_type(self, typedef):
        """ Adds a type definition identified by a given name. """
        types[name] = typedef

    def remove_type(self, name):
        """ Removes a type definition given its name. """
        return types.pop(name, None)

    def get_type(self, name):
        """ Gets type definition by its name. """
        return types.get(name)

default_types = []
