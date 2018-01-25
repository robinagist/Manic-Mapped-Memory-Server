import hashlib, xxhash, sha3
import config
from manic.exceptions import ManicCryptograhicError

# crypto functions for Manic

# use xxhash and md5 for non-crypto digests


def nc_hash(str, seed=0):

    str = bytes(str, 'utf-8')

    if config.NON_CRYPTO_HASH == config.XXHASH:
        return xxhash.xxh64(str, seed=seed).hexdigest()
    elif config.NON_CRYPTO_HASH == config.MD5:
        # open-ssl barfs on short method, so do it longhand.  no seeding
        h = hashlib.md5()
        h.update(str)
        return h.hexdigest()

    # a default non-crypto hash has not been set
    msg = "config.NON_CRYPTO_HASH is not configured to config.XXHASH or config.MD5"
    raise ManicCryptograhicError(msg)


def page_hash(page, seed=0):
    pass