# Evolvers

Evolution simulation inspired by <a href="https://www.youtube.com/watch?v=C9tWr1WUTuI"> the Evolv.io project from carykh </a> (<a href="https://github.com/carykh/EvolutionSimulator2D">original Github repo</a>) remade in Python using Pygame.

<h4><b> WARNING: </b> This is my original version from 2019 and 2020. The code is extremely bad and unreadable!</h4>

<p><i> (14-year-old me didn't really know what structuring was) </i></p>

<br/>

A reworked and restructured version (created in 2020, 2021 and 2023) will be uploaded soon.


<h2> How to run </h2>

<h4> Prerequisites: Python 3.6 or higher with pip installed </h4>

<h3> Install the required packages </h3>

Execute in a terminal:

    pip install -r requirements.txt

If you have multiple Python versions installed, you might have to specify the specific install in the command (e.g <code>pip3</code> for Python 3 or <code>pip3.7</code> for Python 3.7 specifically).

<h3> Run the GUI </h3>

Open Evolvers/run.py

<h3> Optional: Configure language settings </h3>

Once the GUI has been run at least once, the config file can be edited.

Open <code>Evolvers/config.json</code> and change the <code>"language"</code> value.

<h3> Valid languages </h3>

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
