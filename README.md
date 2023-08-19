# Evolvers

Evolution simulation inspired by <a href="https://www.youtube.com/watch?v=C9tWr1WUTuI"> the Evolv.io project from carykh </a> (<a href="https://github.com/carykh/EvolutionSimulator2D">original Github repo</a>) remade in Python using Pygame.

#### This is an early version of v2. For the original version from 2019 and 2020, switch to branch <code>v1</code>


## How to run

#### Prerequisites: Python 3.7 or higher with pip installed

### Install the required packages

Execute in a terminal:

    pip install -r requirements.txt

If you have multiple Python versions installed, you might have to specify the Python installation you want to use in the command (e.g <code>pip3</code> for Python 3 or <code>pip3.7</code> for Python 3.7 specifically).

### Run the GUI

Open Evolvers/run_v2.py

## How to build

Building requires additional dependencies. These can be installed by running

    pip install -r requirements_build.txt

As specified in the "How to run" section, you might have to specify the installation you want to use.

Building itself is as easy as running

    cd Evolvers
    python setup.py build

This will create a build for your current operating system under the <code>build/</code> subdirectory.
Building takes less than a minute on a modern Windows PC, but can take over 30 minutes on low-power systems such as the Raspberry Pi.

## More documentation will be added soon.