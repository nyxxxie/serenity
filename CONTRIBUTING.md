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
Spade attempts to make use of the convention and layouts popular in other
projects.  The hardest part about getting started will likely be getting familar
enough with the codebase to understand how you might contribute an improvement
or idea you have.  We reccomend the following to understand what's going on:
  * Check out [this document] for a description of how the repo is organized.
    Use this to hone in on areas that might be relevant to your proposed
    contribution and to understand where it might belong.
  * When trying to learn about a method or class, how you learn it depends on the
    reason why you need to learn about it:
      1. *What is it for?* All documented components should explain their
         purpose, so check the generated sphinx docs or the docstrings
         associated with that component.
      2. *How do I use it?* First check out the docs for that method, and then
         check out the relevant tests associated with it and its usages in the
         codebase.
      3. *How does it work?* Read the code, which should be sufficiently
         commented that you can understand what it's doing.
    As you contribute yourself, keep these assumptions of how a component will
    be documented in mind so that other developers can expect the same
    experience when reading your code.  Code that isn't sufficiently documented
    *is a valid issue* and may be raised in the issue tracker.

### Task ideas
If you want to contribute but don't know where to start, here are some tasks
that you can do right now without needing to be too creative:
  * Solve or lend your expertise to an issue in the issue tracker.
  * Review open pull requests (including those in progess).
  * Implement approved features in the issue tracker (if they don't already
    have a pull request open)
  * Create new tests for cases we don't cover.  You can easily assess this using
    pytest-cov.  Check out Testing section for more info.

The biggest challenge to getting started is getting to know the codebase well
enough to feel comfortable contributing.  Here are some low-complexity tasks
that you may consider engaging in to help become familiar with spade:
  * Create new tests
  * Investigate/fix low complexity bugs
  * Implement approved feature requests

## Feature requests
If you have an idea for a feature you would like to see in spade or would like
to implement, submit an issue.  Approved feature requests will be given the
cooresponding label.  If no one is assigned and there are no [wip] pull
requests for that issue, feel free to implement it.

When developing features, prioritize ease of use and usefulness in your
decisions.  For example, if you're adding a new api function, you should be
able to imagine a use case for it that necessitates its addition.  This is
especially true when such decisions complicate the api for new users.

When submitting a feature, please ensure all tests pass and pylint doesn't
complain about anything.  You'll have to fix those things anyways when they
don't pass for your reviewer anyways, so may as well do it sooner rather than
later!

## Pull requests
If you want to contribute code, use pull requests.  Pull requests should be
used to make others aware of your work on a code change or to ask for feedback
on a change.  If your feature is in progress, please prefix your pull request
with [WIP].  If you have an idea with no code or do not intend to work on the
feature, use the issue tracker.  Make all your changes in a topic branch as
opposed to master.

## Bug patching
A good way to contribute and get familiar with spade's internals is to
investigate and patch bugs.  Contribute bug patches just as you would
contribute any other code, but please also include a unit test to test for the
bug in question.  When a bug is submitted to the issue tracker, it will be
rated and assigned if applicable.  Before you start your patch, ensure there
are no [wip] pull requests opne for that bug and that no one is assigned to it.

## Testing
Spade requires that all major code additions or modifications be accompanied by
tests.  Tests make life easier for all parties because it helps us ensure your
code is working, helps future developers ensure their code doesn't break
anything, and gives new developers pseudo-documentation to reference when trying
to understand your api.

When writing tests or determining how to test your code, it's suggested that you
start by testing expected common invocations and edge cases that your method
might face.  You should then fill in the gaps using coverage informtation to
determine what lines of code aren't being exercised.  Spade uses pytest-cov for
generating coverage info, check out the docs on how to use it [here][10].

We reccomend adopting a test-driven development workflow so that your tests keep 
up with the code you write, and serve to actually help you develop rather than 
provide a chore when your feature is ready.  When designing tests, please try to
cover each code path in each function (unit tests) as well as test against weird 
inputs.  Also write tests to make sure your components interact properly with
any other associated components (integration tests).

If you are looking for a low-complexity way to start working on spade, creating
new tests for existing code is an excellent and useful way to do so!

## Branching
Please implement all features in feature branches named with the template
`<type>/<name>`.  Valid types include:
  * `feature` - For use on branches that add new functionality or improvements
    to spade
  * `bug` - For use on branches that are intended to address a bug.
  
Please use the `<name>` field to reference an issue number, especially for bugs.
If you want to contribute a feature and there is no issue for it in the issue
tracker, you may use a descriptive english name for `<name>` 
(EG: `feature/new_widget`).  Favor underscores over dashes for spaces.

## Code style
Code must adhere to [PEP8][4] with the following additions/exceptions:
  * Use `import`s for packages and modules only.  This makes namespace
    management simpler, as the source of each identifier is indicated in a
    consistent way (e.g. `blah.Thing` says that `Thing` is defined in `blah`).
  * Line length is limited to 79 chars, however this restriction may be lifted
    ignored if it would result in ugly code.  For example, if you add a comment
    to a line that increases that line's length to 100, that is acceptable.
    The pylint config bundled with this repo defaults to 80, so if you go over
    and trigger a warning please make sure there's a good reason for it.
  * Class methods must be declared in the following order:
      1. Special class methods (`__init__`, `__str__`, etc)
      2. Public class methods
      3. Private class methods (prefixed with _)
  * Refrain from using double underscore prefixes for methods and variables.
  * Please use [type hints][7] whenever you expect an argument to be of a
    specific type.
  * Please comment anything that wouldn't be immediately apparant to the average
    python programmer who has little-to-no experience with this codebase.  This
    is mostly left to your best judgement, but please be considerate and note
    that it's far better to have too many comments than barely any comments.
  * Do not use periods at the end of a comment unless your comment consists of
    multiple sentences or is long.  This is both because most comments aren't
    complete sentences and because the period at the end looks bad when the
    comment is smaller.  This is more of a best judgement kind of thing, so do
    what you feel is right.
  * It is preferred that all "blocks" of code that perform a distinct task
    should have comment inserted before them explaining their purpose.  This
    makes it easier to read code quickly and understand what the author
    intended for it to do.  It also readability, since it's easy to deliniate
    what blocks perform what specific functionality.
  * Prefer `format` to `%`.
  * Avoid huge methods.  Split out functionality into private or helper methods
    if a particular block in a function is performing a large task, even if it's
    only used in one specific area.
  * Use exceptions only in cases where a method failing is a potentially fatal
    action, where fatal is defined as the program entering an invalid state.
    The program crashing is FAR preferable to it functioning incorrectly and
    creating difficult to diagnose bugs.
  * NEVER throw an Exception, subclass it or use an existing subclassed
    exception relevant to your error.
  * Use spaces for indents.  Tabs are great because they are one byte and can
    be set to appear to be any number of spaces you prefer, but that same
    flexibility breaks style when people use spaces to align arguments and
    conditionals.  This mixing isn't even allowed in Python3.
  * If you need to wrap a function or conditional that goes over the 80 char
    limit, please adhere to the following style.  Notice:
      1. All wrappe lines are double indented.  This is to distinquish them
         from the next line.
      2. No words are cut off in the middle and continued on the next line.
         This is to increase readability.  Be sure to und your wrapped string
         line with a space!
      3. If it makes sense, you may start typing arguments on the next line.
         This is acceptable if proportionally the size of arguments don't match
         up or if a function invocation is exceptionally long and there is
         little room for the first argument.  Avoid the latter if there are
         only a few arguments, however.

```python
var = HugeFunctionCall(("This is a massive string that will wrap.  It "
        "displays the value of some variable to via format, so notice how we "
        "enclose it in parens!  Here's that value: {}.").format(value))
    #do stuff
```

## Documentation
All methods and classes should have docstrings written for them.  As spade
currently uses [sphinx][8] for generating documentation, docstrings will be
displayed as [reStructuredText][9].  Docstrings, therefore,  may make use it's
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

## Bug reporting
Please note that the issue tracker is *not* tech support.  Please only report
faults or issues in spade itself.  When you report, please use [this template][5]
to give us information necessary to diagnose and fix your bug.  If you have
found a potential bug related to security, please email `nyxxxxie at gmail`
directly.  Nyxxie's public key can be found on [keybase][6].

[1]:  https://github.com/nyxxxie/spade
[2]:  https://docs.python-guide.org/en/latest/dev/virtualenvs/
[3]:  http://nvie.com/posts/a-successful-git-branching-model/
[4]:  https://www.python.org/dev/peps/pep-0008/#code-lay-out
[5]:  BUG_TEMPLATE.txt
[6]:  https://keybase.io/nyxxie/
[7]:  https://www.python.org/dev/peps/pep-0484/
[8]:  http://www.sphinx-doc.org
[9]:  http://www.sphinx-doc.org/en/stable/rest.html
[10]: https://pypi.python.org/pypi/pytest-cov#usage
