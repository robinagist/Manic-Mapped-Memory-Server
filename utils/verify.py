from utils import crypto
from manic import exceptions

def verify_file(mapped_file, verifyfile):
    '''
    uses the generated hashes to verify that the file is authentic and has not been tampered with
    :param scorefile: full path to the mappedfile
    :param verifyfile: full path to the verifyfile
    :param bypass: if True, bypasses verification

    :return: True if good, or False if hash doesn't match file
    '''

    # no verify file configured or missing will bypass the verification
    if not verifyfile:
        raise exceptions.ManicVerificationError("verification file not set")
    try:
        vf = open(verifyfile, "r")
    except:
        raise exceptions.ManicVerificationError("missing or misconfigured verify-hash.txt file")

    errors = []

    # grab the hash
    vf_hash = vf.readline().strip()
    sf_calculated_hash = crypto.secure_file_hash(mapped_file)

    if vf_hash != sf_calculated_hash:
        errors.append(vf_hash)
        errors.append(sf_calculated_hash)

    return errors


# helper - returns the verify file full path
def verify_filename(config):
        return config["verifyfile"]


# verification helper -- error blurb
def verify_errors(errors):
        print("VERIFICATION ERROR: calculated hash does not match provided hash")
        print("     verified hash: {}".format(errors[0]))
        print("   calculated hash: {}".format(errors[1]))
        print()
        print("cannot load score file -- it's authenticity cannot be verified")
        exit(1)


# helper - bypass verify
def bypass_verify(config):
    return config["bypass-verify"]
