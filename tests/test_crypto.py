import config
from utils import crypto


def test_01_md5():
    config.NON_CRYPTO_HASH = config.MD5
    str = "i am a test string"
    seed = 0

    res = crypto.nc_hash(str, seed)

    assert res is not None

def test_02_md5_default_seed():
    config.NON_CRYPTO_HASH = config.MD5
    str = "i am a test string"
    seed = 0

    res1 = crypto.nc_hash(str, seed)
    res2 = crypto.nc_hash(str)

    assert res1 == res2


def test_03_xxhash():
    # change the default hash
    config.NON_CRYPTO_HASH = config.XXHASH
    str = "i am a test string"
    seed = 0

    res = crypto.nc_hash(str, seed)

    assert res is not None

def test_02_xxhash_default_seed():
    config.NON_CRYPTO_HASH = config.XXHASH
    str = "i am a test string"
    seed = 0

    res1 = crypto.nc_hash(str, seed)
    res2 = crypto.nc_hash(str)

    assert res1 == res2
