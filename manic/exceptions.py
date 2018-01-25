

class ManicChainingError(Exception):
    def __init__(self, msg=None):
        if not msg:
            msg = "Duplicate values are not allowed in columns declared `UNIQUE`"
        Exception.__init__(self, msg)


class ManicIndexingError(Exception):
    def __init__(self, msg=None):
        if not msg:
            msg = "Duplicate names are not allowed for column-indexes within or across mapped files"
        Exception.__init__(self, msg)


class ManicPageProtectedError(Exception):
    def __init__(self, msg=None):
        if not msg:
            msg = "Mapped file is write protected at the page level"
        Exception.__init__(self, msg)


class ManicCryptograhicError(Exception):
    def __init__(self, msg=None):
        if not msg:
            msg = "cryptographic settings are not properly configured"
        Exception.__init__(self, msg)
