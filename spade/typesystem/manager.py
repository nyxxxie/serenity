from spade.typesystem.types import default_types

class TypeManager:
    def __init__(self):
        self._types = []
        self._add_default_types()

    def _add_default_types(self):
        for typedef in default_types:
            self.add_type(typedef)

    def add_type(self, typedef):
        """
        Adds a type definition identified by a given name.
        """
        self._types.append(typedef)

    def remove_type(self, name):
        """
        Removes a type definition given its name.
        """
        for typedef in self._types:
            for tname in typedef.names:
                if tname == name:
                    return self._types.remove(typedef)

        return None

    def get_type(self, name):
        """
        Gets type definition by its name.
        """
        for typedef in self._types:
            for tname in typedef.names:
                if tname == name:
                    return typedef

    def types(self):
        """
        Returns the string identifiers of all types currently registered.
        """
        names = []
        for typedef in self._types:
            names.extend(typedef.names)

        return names
