
# Manic - Hella Fast Memory Mapped Lookup Server

Manic is a asynchronous REST server that allows super fast querying of large memory mapped files, giving O(1) lookup times on the order of 5-10 microseconds (local server response around 1ms), using standard desktop hardware.

Manic runs on top of [Sanic, a super fast, Flask-like async platform for Python](https://github.com/channelcat/sanic)

Even more, Manic allows you to write protect the file in memory at the page level, and check a previously calculated SHA256 of the text file, against your own SHA256, before it is loaded into a memory map, providing hella fast lookups in the single digit microsecond range on your laptop.

Manic was extracted from an Ethereum oracle project I am working on, and made open source under an MIT license.  The functionality has been enhanced beyond the original requirements for the oracle.  This repo is still a work in progress, but Manic is fully working and functional for your fast lookup use cases, and can load files in sizes up to the memory capacity you have on hand.

At the moment, Manic will only ingest and index delimited text files.

***Real documentation is in the works, I promise***

## run it!

+ clone the repo `git@github.com:robinagist/Manic-Mapped-Memory-Server.git`
+ high recommended that you run Manic in virtualenv with at least Python 3.5
+ install Sanic `pip install sanic`
+ install pysha3 `pip install pysha3`
+ install xxhash `pip install xxhash` 
+ Manic is already configured to index two example files in the `/manic/memfiles` directory
+ configure the `BASE_PATH` in `config.py` to point to your local `manic` root
+ from the `manic` directory, start the server: 'python server.py` which will immediately index the files
+ the server listens on port `5216` by default
+ the query string on the URL for the server will be of the format:
```
idx=<index_name>&st=<search term>
```
Index_name is the column you wish to perform a lookup. Column names are index names.


Manic comes with two example files:  a short list of poker hands and scores, and a subset of the FCC database for ham radio licenses.  It is configured to run right out of the box with those.

  try `curl "http://0.0.0.0:5216/f?idx=call&st=KC1IVY"` from a terminal, to do a callsign lookup.  you should get one result
  
  or try `curl "http://0.0.0.0:5216/f?idx=cat&st=D"` and you should get around 250 results
  
Each column name is also the index name.  To do a lookup on a column -- say for an FCC callsign -- use the `call` column and the search term `st` is an FCC assigned callsign, hopefully appearing in the file.  The columns are defined in the configuration file `config.json` for the file that is being indexed.  These are located in the `~/memfiles` subdirectory.

More documentation later.






