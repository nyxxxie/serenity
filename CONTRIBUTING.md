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
```
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
that you may consider engaging in to help become familiar with:
  * blah1
  * blah2

Mycroft also supports sphinx documentation generation, which you may find
useful.  To build documentation, simply execute `python setup.py build_sphinx`.


[1]: https://github.com/nyxxxie/spade
[2]: http://docs.python-guide.org/en/latest/dev/virtualenvs/
