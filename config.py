
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

# indexing and constraints
DEFAULT = 0b00000000
NOINDEX = 0b00000001
UNIQUE  = 0b00000010



# hashing and verification
SHA1 = 1
SHA3 = 2
SHA256 = 3
MD5 = 10

PAGE_HASHING   = SHA1
LINE_HASHING   = MD5
COLUMN_HASHING = MD5



BASE_PATH = "/Users/robin/PycharmProjects/manic"
MEMFILES_DIR = "memfiles"

HOST = "0.0.0.0"
PORT = 5216
KEEP_ALIVE = 0

LOGLEVEL = INFO            # DEBUG|INFO|WARN|ERROR|OFF
LOGOUTPUT = "log.txt"      # filename|NONE (for websockets)
LOGFORMAT = FORMAT_JSON    # TEXT|JSON


# admin
ADMINABLE = False
ADMIN_PORT = 52164
ALLOW_SHUTDOWN = False


