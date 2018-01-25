import hashlib, xxhash, sha3, rsa
import config
from manic.exceptions import ManicCryptograhicError

# crypto functions for Manic

# use xxhash and md5 for non-crypto digests


def non_c_hash(str, seed=0):

    str = bytes(str, 'utf-8')

    if config.NON_CRYPTO_HASH == config.XXHASH:
        return xxhash.xxh64(str, seed=seed).hexdigest()
    elif config.NON_CRYPTO_HASH == config.MD5:
        # open-ssl barfs on short method, so do it longhand.  no seeding
        h = hashlib.md5()
        h.update(str)
        return h.hexdigest()

    # a default non-crypto hash has not been set
    msg = "config.NON_CRYPTO_HASH is not configured"
    raise ManicCryptograhicError(msg)


def c_hash(str, seed=0, size=32):

    if config.CRYPTO_HASH == config.SHA3_256:
        h = hashlib.sha3_256()
        h.update(str)
        return h.hexdigest()

    # a default non-crypto hash has not been set
    msg = "config.CRYPTO_HASH is not configured"
    raise ManicCryptograhicError(msg)


def secure_file_hash(filename):
    '''
    reads the score file and generates a SHA1 hash
    :param filename: filename to hash
    :return: the hash value of the file
    '''
    BUF_SIZE = 65535*4

    if config.SECURE_FILE_HASH == config.SHA256:
        h = hashlib.sha256()
    elif config.SECURE_FILE_HASH == config.SHA1:
        h = hashlib.sha1()
    else:
        msg = "config.SECURE_FILE_HASH not set to SHA1 or SHA256"
        raise ManicCryptograhicError(msg)

    with open(filename, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            h.update(data)
        return h.hexdigest()

