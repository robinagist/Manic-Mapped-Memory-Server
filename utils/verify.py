import hashlib


def hashfile(filename):
    '''
    reads the score file and generates a SHA1 hash
    :param filename: filename to hash
    :return: the hash value of the file
    '''
    BUF_SIZE = 65535*4
    sha1 = hashlib.sha1()

    with open(filename, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
            return sha1.hexdigest()


def verify_file(mapped_file, verifyfile, bypass=False):
    '''
    uses the generated hashes to verify that the file is authentic and has not been tampered with
    :param scorefile: full path to the mappedfile
    :param verifyfile: full path to the verifyfile
    :param bypass: if True, bypasses verification

    :return: True if good, or False if hash doesn't match file
    '''

    # no verify file configured or missing will bypass the verification
    if not verifyfile or bypass:
        return None, bypass

    vf = open(verifyfile, "r")

    errors = []

    # grab the hash
    vf_hash = vf.readline().strip()

    sf_calculated_hash = hashfile(mapped_file)

    if vf_hash != sf_calculated_hash:
        errors.append(vf_hash)
        errors.append(sf_calculated_hash)

    return errors, bypass


# helper - returns the verify file full path
def verify_filename(config):
        return config["memmap"]["verifyfile"]


# verification helper -- error blurb
def verify_errors(errors):
        print("VERIFICATION ERROR: calculated hash does not match provided hash")
        print("     verified hash: {}".format(errors[0]))
        print("   calculated hash: {}".format(errors[1]))
        print()
        print("cannot load score file -- it's authenticity cannot be verified")
        exit(1)
