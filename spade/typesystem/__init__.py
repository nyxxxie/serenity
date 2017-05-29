from spade.typesystem.manager import TypeManager
typemanager = TypeManager()

# Add default types to typemanager.  The __init__.py in this directory imports
# all types, and each type adds itself into the typemanager object.  Is this
# hacky?  I dunno, but it works!
import spade.typesystem.types
