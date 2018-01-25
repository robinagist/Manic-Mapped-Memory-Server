import pytest
from utils import data


def test_01_define_columns():

    cols = ["col1", "col2", "colA", "col3"]
    d = data.define_columns_using_delimiter(cols)
    assert d is not None


def test_02_define_columns_more():

    cols = ["col1", "col2", "colA", "col3"]

    d = data.define_columns_using_delimiter(cols)

    assert d is not None
    ee = d["indexes"]
    assert ee is not None

    assert ee[0] == "col1"

    data.define_skip_startlines(1,d)
    assert d["skip"] == 1
    data.define_chomp_lastlines(1,d)
    assert d["chomp"] == 1

