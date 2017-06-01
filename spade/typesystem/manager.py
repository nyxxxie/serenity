class TypeManager:
    def __init__(self):
        self._types = []

    def add_type(self, typedef):
        """
        Adds a type definition identified by a given name.
        """
        return self._types.append(typedef)

    def remove_type(self, name):
        """
        Removes a type definition given its name.
        """
        for t in self._types:
            for tname in t.__typenames__:
                if tname == name:
                    return self._types.remove(tname)

        return None

    def get_type(self, name):
        """
        Gets type definition by its name.
        """
        for t in self._types:
            for tname in t.__typenames__:
                if tname == name:
                    return t

        return None

    def types(self):
        """
        Returns the string identifiers of all types currently registered.
        """
        return [t.typedef for t in self._types]
