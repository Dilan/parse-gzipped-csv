Command line tool that takes one parameter which is an URL to a gzipped CSV file
stored on a remote server.

● The program must download this gzipped CSV file
● The file will contain data about each user with various bits of information
    ○ user_id
    ○ date_joined
    ○ spend
    ○ milliseconds played
    ○ device_height ­ px
    ○ device_width ­ px
● Your program should then output to standard out the following with new line separators
    ○ Total count of all users
    ○ number of users with a device resolution of 640x960
    ○ total spend of all users in dollars
    ○ user_id of the first user who joined
● Your program should have sufficient unit tests, with a good coverage. Feel free to use whatever unit testing framework you like or none at all.
● Your program should treat all data it receives as untrustworthy and unsanitized.
● Your program should run in a timely manner.
● Your program should handle common failure cases (returning a non­zero exit status).

Start
-----

    $ python src/download.py "https://github.com/Dilan/parse-gzipped-csv/files/428251/test.csv.gz"

Tests
-----

    $ python -m unittest test.test_download

Servers
-------

    $ cd server/
    $ npm install

    // Server 1: send 0.5Kb chunk and after 3 seconds confirm stream end
    $ node chunk-stream.js 1337
    // read:
    $ python src/download.py "http://127.0.0.1:1337"

    // Server 2: send with 1 second delay
    $ node delay-stream.js 1338
    // read:
    $ python src/download.py "http://127.0.0.1:1338"
