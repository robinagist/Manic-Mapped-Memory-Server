import os
'''
Manic configuration
'''

# loglevels
DEBUG = 1
INFO  = 2
WARN  = 3
ERROR = 4
OFF   = 5

# log formats
FORMAT_JSON = 1
FORMAT_TEXT = 2

# hashing and verification
SHA1 = 1
SHA3_256 = 2
SHA256 = 3

# non crypto hashing
MD5 = 10
XXHASH = 11

NON_CRYPTO_HASH = XXHASH
CRYPTO_HASH = SHA3_256
SECURE_FILE_HASH = SHA256

BASE_PATH = "{}/".format(os.getcwd())

MEMFILES_DIR = "memfiles"

HOST = "0.0.0.0"
PORT = 5216
KEEP_ALIVE = 1



