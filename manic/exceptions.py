

class ManicChainingError(Exception):
    def __init__(self, msg=None):
        if not msg:
            msg = "Duplicate values are not allowed in columns declared `UNIQUE`"
        Exception.__init__(self, msg)


class ManicIndexingError(Exception):
    def __init__(self, msg=None):
        if not msg:
            msg = "Duplicate names are not allowed for columns within or across files"
        Exception.__init__(self, msg)


