## Documentation
All methods and classes should have docstrings written for them.  As spade
currently uses [sphinx][1] for generating documentation, docstrings will be
displayed as [reStructuredText][2].  Docstrings, therefore,  may make use it's
markup to add emphasis, charts, code examples, etc to their docstrings.

Documentation may be generated using the Makefile in the `docs` folder, or 
alternately by using the command `python setup.py build_sphinx`.  Generated
documentation will be located in `docs/.build/<type>/`, where `<type>` is the
type of documentation that was generated (html, manpages, etc).

### Methods
Docstrings for methods should describe that method's purpose, arguments, and 
return value at minimum.  A good rule of thumb to follow is that a user should
know when and how to use a method simply by looking at its signature and
docstring.  The following is an example of an acceptable dostring:
```python
    def seek(self, offset: int=0, from_what: int=0) -> int:
        """
        Sets the cursor position relative to some position.

        :param offset: Offset into file relative to from_what parameter.
        :param from_what: Determines what the above offset is relative to.
        :return: Cursor position after the seek operation completes.

        The reference point specified by the ``from_what`` parameter should
        take on one of the following values:

            * 0 - Offset from beginning of file.
            * 1 - Offset from current cursor position.
            * 2 - Offset from end of file.

        The ``from_what`` parameter may be omitted, and will default to 0
        (beginning of file).
        """
```

### Classes
Docstrings for classes should describe that class's purpose in the project.  A
rule of thumb to go by with class docstrings is that a developer should be able
to know exactly what the class is for and how it is meant to be used by reading
the docstring by itself.

[1]:  http://www.sphinx-doc.org
[2]:  http://www.sphinx-doc.org/en/stable/rest.html
