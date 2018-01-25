import pytest
from utils import data


def test_define_columns():

    cols = ["col1", "col2", None, "col3"]
    d = data.define_columns_using_delimiter(cols)
    assert d is not None


def test_define_columns_more():

    cols = ["col1", "col2", None, "col3"]
    d = data.define_columns_using_delimiter(cols)

    assert d is not None
    ee = d["names"]
    assert ee is not None
    assert ee[0] == "col1"

    data.define_skip_startlines(1,d)
    assert d["skip"] == 1
    data.define_chomp_lastlines(1,d)
    assert d["chomp"] == 1

