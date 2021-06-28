
Utility to create a SQLite database with the name of your LinkedIn connection along with additional notes you want to keep.
For instance, "Met at the IEEE 2021 conference in Barrow, Alaska"

To begin, download a copy of your data from LinkedIn.
    Go to Account -> Settings and Privacy -> Get a copy of your data

In the downloaded data, look for a file Connections.csv. This file contains the relevant information and will be used to create the sqlite database.

To create the initial database:

    python3 linotes.py -c

To read everything:

    python3 linotes.py -r

To find a person by name, specify the first and last name. You can also specify a partial string, e.g.:

    python3 linotes.py -p -F John -L Doe

    python3 linotes.py -p -F John -L Do

To add a note to a connection by name, specify the first name, last name, and the note. e.g.:

    python3 linotes.py -a -F John -L Doe -n "Met at the IEEE 2021 conference in Barrow, Alaska"

