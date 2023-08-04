# Evolvers

Evolution simulation inspired by <a href="https://www.youtube.com/watch?v=C9tWr1WUTuI"> the Evolv.io project from carykh </a> (<a href="https://github.com/carykh/EvolutionSimulator2D">original Github repo</a>) remade in Python using Pygame.

#### <b> WARNING: </b> This is my original version from 2019 and 2020 (referred to v1 in documentation). The code is extremely bad and unreadable! 

<i> (14-year-old me didn't really know what structuring was) </i>

<br/>

A reworked and restructured version (created in 2020, 2021 and 2023) will be uploaded soon.


## How to run

#### Prerequisites: Python 3.6 or higher with pip installed

### Install the required packages

Execute in a terminal:

    pip install -r requirements.txt

If you have multiple Python versions installed, you might have to specify the Python installation you want to use in the command (e.g <code>pip3</code> for Python 3 or <code>pip3.7</code> for Python 3.7 specifically).

### Run the GUI

Open Evolvers/run.py

### Optional: Configure language settings

Once the GUI has been run at least once, the config file can be edited.

Open <code>Evolvers/config.json</code> and change the <code>"language"</code> value.

### Valid languages

<table>
    <tr>
        <th>
            Value
        </th>
        <th>
            Language
        </th>
    </tr>
    <tr>
        <td>
            <code>STD</code>
        </td>
        <td>
            Default language baked into the python file (English, as long as unchanged)
        </td>
    </tr>
    <tr>
        <td>
            <code>DE</code>
        </td>
        <td>
            Deutsch / German
        </td>
    </tr>
    <tr>
        <td>
            <code>ENG</code>
        </td>
        <td>
            English
        </td>
    </tr>
</table>

Additional languages can be implemented by creating a <code>[Language Code].lang</code> file by following the JSON-like structure in the other files and setting the config value to that language code.

Evolvers will load the <code>STD</code> language if there is a syntax error in your language file.


## How to build

Building requires additional dependencies. These can be installed by running

    pip install -r requirements_build.txt

As specified in the "How to run" section, you might have to specify the installation you want to use.

Building itself is as easy as running

    cd Evolvers
    python setup.py build

This will create a build for your current operating system under the <code>build/</code> subdirectory.
Building takes less than a minute on a modern Windows PC, but can take over 30 minutes on low-power systems such as the Raspberry Pi.

