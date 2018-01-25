import config, pytest
from utils import crypto
from manic import exceptions


def test_01_md5():
    config.NON_CRYPTO_HASH = config.MD5
    str = "i am a test string"
    seed = 0

    res = crypto.non_c_hash(str, seed)

    assert res is not None

def test_02_md5_default_seed():
    config.NON_CRYPTO_HASH = config.MD5
    str = "i am a test string"
    seed = 0

    res1 = crypto.non_c_hash(str, seed)
    res2 = crypto.non_c_hash(str)

    assert res1 == res2


def test_03_xxhash():
    # change the default hash
    config.NON_CRYPTO_HASH = config.XXHASH
    str = "i am a test string"
    seed = 0

    res = crypto.non_c_hash(str, seed)

    assert res is not None

def test_04_xxhash_default_seed():
    config.NON_CRYPTO_HASH = config.XXHASH
    str = "i am a test string"
    seed = 0

    res1 = crypto.non_c_hash(str, seed)
    res2 = crypto.non_c_hash(str)

    assert res1 == res2

def test_05_non_crypto_bad_configure_setting():
    # change the default hash
    config.NON_CRYPTO_HASH = 2908320498

    with pytest.raises(exceptions.ManicCryptograhicError) as e:
        res = crypto.non_c_hash("test")

def test_06_sha3_256():

    config.CRYPTO_HASH = config.SHA3_256
    str = "i am a test string".encode("utf-8")

    res = crypto.c_hash(str)

    assert res is not None



def test_08_crypto_bad_configure_setting():
    # change the default hash
    config.CRYPTO_HASH = 2908320498

    with pytest.raises(exceptions.ManicCryptograhicError) as e:
        res = crypto.c_hash("test")
