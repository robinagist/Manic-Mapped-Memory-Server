
# Manic - Hella High Performance Memory Mapped Lookup Server

Manic is a asynchronous REST server that allows super fast querying of large memory mapped files, giving O(1) lookup times on the order of 5-10 microseconds, using standard desktop hardware.

Manic runs on top of [Sanic, a super fast, Flask-like async platform for Python](https://github.com/channelcat/sanic)

Even more, Manic allows you to write protect the file in memory at the page level, and check a previously calculated SHA256 of the text file, against your own SHA256, before it is loaded into a memory map, providing hella fast lookups in the single digit microsecond range on your laptop.

Manic was extracted from an Ethereum oracle project I am working on, and made open source under an MIT license.  This repo is still a work in progress, but Manic is fully working and functional for your fast lookup use cases.

At the moment, Manic will only ingest and index delimited text files.

## Configuration is simple:

+ clone the repo
+ Manic is already configured to index two example files in the `/manic/memfiles` directory
+ in the `/manic/memfiles` directory, create a subdirectory
+ drop in your delimited file (or use the examples)
+ in your flat-file, determine the number of fields in a row of data, separated by a delimiter
+ determine the names of the data columns, which ones should be constrained `UNIQUE` and which ones shouldn't index (`NOINDEX`)
+ put a copy of one of the `config.json` files in the directory and fill in with the data from the last instruction
+ start the server, which will immediately index the file
+ the server listens on port `5216` by default
+ the query string on the URL for the server will be of the format:
```
idx=<index_name>&st=<search term>
```
where index_name is the column you wish to perform a lookup. 

  e.g. `http://0.0.0.0:5216/f?idx=hand&st=JH-KS-QC-QS-TH`

+ use curl or a browser to get the result

Manic comes with two example files:  a short list of poker hands and scores, and a subset of the FCC database for ham radio licenses.  It is configured to run right out of the box with those.





