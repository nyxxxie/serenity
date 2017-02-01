# Contributing
Spade welcomes all kinds from contributions from anyone who wants to
contribute their skill and vision to the tool.  This file serves as a guide
intended to help you figure out how and what to contribute to spade.

## Setting up environment
In order to work on spade, you'll need to set up an environment that'll allow
you to make and submit changes.  Please perform these first initial steps to
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
*TODO: write this*

### Windows
*TODO: write this*

Once your environment is configured, you are ready to start contributing.
Please remember to activate your virtual environment when you want to run
the development version of spade.

## Getting started
The biggest challenge to getting started is getting to know the codebase well
enough to feel comfortable contributing.  Here are some low-complexity tasks
that you may consider engaging in to help become familiar with spade:
  * create unit test
  * investigate/fix low complexity bugs
  * implement approved feature request

Spade also supports sphinx documentation generation, which you may find useful.
To build documentation, simply execute `python setup.py build_sphinx`.

## Unit tests
include them with your code when applicable.  if you want to contribute a unit
tests to test for a potential bug or to strengthen the existing test suite,
feel free

## Branching

## Code style

## Pull requests
If you want to contribute code, it is advised you create a [wip] pull request
so that others know that you are currently working on a specific feature.
Create a feak

## Bug patching

## Feature requests

## Bug reporting
Please note that the issue tracker is *not* tech support.  Please only report
faults or issues in spade itself.  When you report, please use [this template][3]
to give us information necessary to diagnose and fix your bug.  If you have
found a potential bug related to security, please email `nyxxxxie at gmail`
directly.  Nyxxie's public key can be found on [keybase][4].

[1]: https://github.com/nyxxxie/spade
[2]: https://docs.python-guide.org/en/latest/dev/virtualenvs/
[3]: BUG_TEMPLATE.txt
[4]: https://keybase.io/nyxxie/
