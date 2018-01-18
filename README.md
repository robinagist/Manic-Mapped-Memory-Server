
Manic - Hella High Performance Memory Mapped DB Server

Manic is a asynchronous REST server that allows super fast querying of large memory mapped files, giving O(1) lookup times on the order of just a dozen or so microseconds, using standard desktop hardware.

Manic runs on top of Sanic, a super fast, Flask-like async platform for Python https://github.com/channelcat/sanic

Even more, Manic allows you to write protect the file in memory at the page level, and check a previously calculated SHA256 of the text file, against your own SHA256, before it is loaded into a memory map.

Manic was extracted from an Ethereum oracle project I am working on, and made open source under an MIT license.  It is still a work in progress.

At the moment, Manic will only ingest and index delimited text files.

##Configuration is simple:

+ determine the number of fields in a row of data, separated by a delimiter (say, a comma)
+ name each field (these are also the index names, so keep track)
+ start the server, which will immediately index
+ the query string on the URL for the server will be 'idx=<index_name>&st=<search term>
  e.g. http://0.0.0.0:8000/f?idx=hand&st=JH-KS-QC-QS-TH
+ use curl or a browser to get the result:
  
  
###currently:
+ only indexes delimited files
+ does not do partial searches


COMING VERY SOON

+ basic documentation (it's easy to set up your single file for indexing and search, with just configuration of a JSON file -- I just need to show you)
+ multiple file support
+ pip installation
+ automatic column hashing added as an extra column of data in the memmap
+ provide for secure file updating and indexing remotely
+ a testing tool that is already in the works


