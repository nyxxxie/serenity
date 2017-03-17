from spade.typesystem.types import default_types

class TypeManager:
    def __init__(self):
        self._types = {}
        self._add_default_types()

    def _add_default_types(self):
        for typedef in default_types:
            self.add_type(typedef)

    def add_type(self, typedef):
        """
        Adds a type definition identified by a given name.
        """
        self._types[typedef.name] = typedef

    def remove_type(self, name):
        """
        Removes a type definition given its name.
        """
        return self._types.pop(name, None)

    def get_type(self, name):
        """
        Gets type definition by its name.
        """
        return self._types.get(name)

    def types(self):
        """
        Returns the string identifiers of all types currently registered.
        """
        return list(self._types.keys())
