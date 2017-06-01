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


