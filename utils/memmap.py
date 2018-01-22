

# memmap structure helper for multifile

'''
{
	"memmap": {
        "id": "callsigns",
        "pagelocking" : true,
        "type":"delim",
		"filepath": "/Users/robin/poker/test-scores-file.txt",
		"verifyfile": "/Users/robin/poker/verify-hash.txt",
        "indexes": [{
            "name": "hand",
            "constraint": null
          },
          { "name": "score",
            "constraint": "NOINDEX"
          },
          { "name": "hh",
            "constraint": null
          },
          { "name": "hhs",
            "constraint": null
          }
        ],
        "delimiter":",",
        "llnf": true,
        "result-format": "PARSE"
	}
}
'''


def id(mmm):
    return mmm["id"]


def pagelocking(mmm):
    return mmm["pagelocking"]


def filetype(mmm):
    return mmm["type"]


def delimiter(mmm):
    return mmm["delimiter"]


def result_format(mmm):
    return mmm["result-format"]


def memmap_filepath(mmm):
    return mmm["filepath"]


def verify_filepath(mmm):
    return mmm["verifyfile"]


def index_names_list(mmm):
    idxs = mmm["indexes"]
    return [x["name"] for x in idxs]


