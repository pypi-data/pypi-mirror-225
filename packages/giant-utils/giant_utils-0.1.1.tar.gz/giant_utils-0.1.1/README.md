# Giant Utils

A re-usable package which can be used in any django project that allows small common use functions such as an email with text and/or html templates to be sent. 

Other functionality includes a format_bytes method that takes a byte size of file and converts it to a human-readable number with the appropriate Byte suffix (useful for download files).

Also includes a rich text field that can be used in various plugins where the admin may want to insert links or custom html.

## Installation

To install with the package manager, run:

    $ poetry add giant-utils

You should then add "giant_utils" to the `INSTALLED_APPS` in your project's settings file.  Then wherever you want to implement the function you can add the following import statements...

    from giant_utils.sender import send_email_from_template
    from giant_utils.format_bytes import format_bytes
    from giant_utils.fields import RichTextField

## Rich Text Field 

This field can be customised by adding your own WYSIWYG_CONFIG variable to your project's settings. Otherwise it will fallback to the default below...

    DEFAULT_WYSIWYG_CONFIG = {
        "lang": "en",
        "minHeight": "300px",
        "buttons": "html | format | undo redo | bold italic | ul ol | link | sub sup".split(),
        "formatting": ["h1", "h2", "h3", "p"],
        "linkTitle": True,
        "linkNewTab": True,
        "structure": True,
        "removeNewLines": True,
        "pasteImages": False,
        "tabAsSpaces": 4,
        "plugins": ["table"],
    }

## Pre-requisites

The minimum package dependencies for this project are as follows...

- Django 4.0
- python 3.11


## Preparing for release
 
 In order to prep the package for a new release on TestPyPi and PyPi there is one key thing that you need to do. You need to update the version number in the `pyproject.toml`.
 This is so that the package can be published without running into version number conflicts. The version numbering must also follow the Semantic Version rules which can be found here https://semver.org/.
 
## Publishing
 
 Publishing a package with poetry is incredibly easy. Once you have checked that the version number has been updated (not the same as a previous version) then you only need to run two commands.
 
    $ `poetry build` 

will package the project up for you into a way that can be published.
 
    $ `poetry publish`

will publish the package to PyPi. You will need to enter the username and password for the account which can be found in the company password manager