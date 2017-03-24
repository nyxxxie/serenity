# Contributing
Spade welcomes all kinds from contributions from anyone who wants to
contribute their skill and vision to the tool.  This file serves as a guide
intended to help you figure out how and what to contribute to spade.

## Setting up environment
In order to work on spade, you'll need to set up an environment that'll allow
you to make, test and submit changes.  Please perform these first initial steps:
  * Register a github account
  * Fork the main [spade repository][1]
  * Install Python 3.4 or above

For development, we also reccomend setting up a [virtual environment][2].  This
is useful as it allows you to install dependencies and make spade's modules
visible in an environment isolated from the rest of your python projects.  The
process of setting up spade using a virtual environment looks something like
this:

### Linux
```shell
cd <your forked git repo> # Enter project directory
virtualenv venv           # Create virtual environment
. venv/bin/activate       # Activate the virtual environment
pip install -e .          # Install all dependencies and add spade components to path
```

### Mac
```shell
cd <your forked git repo> # Enter project directory
virtualenv venv           # Create virtual environment
. venv/bin/activate       # Activate the virtual environment
pip install -e .          # Install all dependencies and add spade components to path
```

### Windows
*TODO: write this*

Once your environment is configured, you are ready to start contributing.
Please remember to activate your virtual environment when you want to run
the development version of spade.

## Getting started
The biggest challenge to getting started is getting to know the codebase well
enough to feel comfortable contributing.  Here are some low-complexity tasks
that you may consider engaging in to help become familiar with spade:
  * Create new unit tests
  * Investigate/fix low complexity bugs
  * Implement approved feature requests

Spade also supports sphinx documentation generation, which you may find useful.
To build documentation, simply execute `python setup.py build_sphinx`.

## Feature requests
If you have an idea for a feature you would like to see in spade or would like
to implement, submit an issue.  Approved feature requests will be given the
cooresponding label.  If no one is assigned and there are no [wip] pull
requests for that issue, feel free to implement it.

When developing features, prioritize ease of use and usefulness in your
decisions.  For example, if you're adding a new api function, you should be
able to imagine a use case for it that necessitates its addition.  This is
especially true when such decisions complicate the api for new users.

## Pull requests
If you want to contribute code, use pull requests.  Pull requests should be
used to make others aware of your work on a code change or to ask for feedback
on a change.  If your feature is in progress, please prefix your pull request
with [WIP].  If you have an idea with no code or do not intend to work on the
feature, use the issue tracker.  Make all your changes in a topic branch as
opposed to devel or master.

## Bug patching
A good way to contribute and get familiar with spade's internals is to
investigate and patch bugs.  Contribute bug patches just as you would
contribute any other code, but please also include a unit test to test for the
bug in question.  When a bug is submitted to the issue tracker, it will be
rated and assigned if applicable.  Before you start your patch, ensure there
are no [wip] pull requests opne for that bug and that no one is assigned to it.

## Unit tests
Unit tests are a useful way to test code you write.  Not only does it save you
the work of having to write a test client to test your features, but it also
allows future developers to test your features when they may have made changes.
Spade requires that unit tests be submitted with code patches when applicable,
both because of the aforementioned reasons and because it makes it easier to
review pull requests.  If you are looking for a low-complexity way to start
working on spade, creating new unit tests to increase test coverage is an
excellent way to do so!

## Branching
Spade uses the [gitflow][3] development model.  Branches other than develop and
master are to take the form `<type>/<name>`.  Valid types include:
  * `feature` - For use on branches that add new functionality or improvements
    to spade
  * `bug` - For use on branches that are intended to address a bug.
Please use the `<name>` field to reference an issue number, especially for bugs.
If you want to contribute a feature and there is no issue for it in the issue
tracker, you may use a descriptive english name for `<name>` 
(EG: `feature/new_widget`).  Favor underscores over dashes for spaces.

## Code style
Code must adhere to [PEP8][4] with the following additions:
  * Line length is limited to 79 chars, however this restriction may be lifted
    ignored if it would result in ugly code.  For example, if you add a comment
    to a line that increases that line's length to 100, that is acceptable.
  * Class methods must be declared in the following order:
      1. Special class methods (`__init__`, `__str__`, etc)
      2. Public class methods
      3. Private class methods (prefixed with _)
  * Refrain from using double underscore prefixes for methods and variables.
  * Please use [type hints][7] where applicable.
  * Use spaces for indents.

## Documentation
All methods and classes should have docstrings written for them.  As spade
currently uses [sphinx][8] for generating documentation, docstrings will be
displayed as [reStructuredText][9].  Docstrings, therefore,  may make use it's
markup to add emphasis, charts, code examples, etc to their docstrings.

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

## Bug reporting
Please note that the issue tracker is *not* tech support.  Please only report
faults or issues in spade itself.  When you report, please use [this template][5]
to give us information necessary to diagnose and fix your bug.  If you have
found a potential bug related to security, please email `nyxxxxie at gmail`
directly.  Nyxxie's public key can be found on [keybase][6].

[1]: https://github.com/nyxxxie/spade
[2]: https://docs.python-guide.org/en/latest/dev/virtualenvs/
[3]: http://nvie.com/posts/a-successful-git-branching-model/
[4]: https://www.python.org/dev/peps/pep-0008/#code-lay-out
[5]: BUG_TEMPLATE.txt
[6]: https://keybase.io/nyxxie/
[7]: https://www.python.org/dev/peps/pep-0484/
[8]: http://www.sphinx-doc.org
[9]: http://www.sphinx-doc.org/en/stable/rest.html
