import pytest
import ampcountpy
#python -m pytest

def test_initValues():
    assert ampcountpy.initValues(0,0) == 0
    assert ampcountpy.initValues(0,1000) == 0
    assert ampcountpy.initValues(1,0) == 1
    assert ampcountpy.initValues(1,1000) == 1
    assert ampcountpy.initValues(10,0) == 10
    assert ampcountpy.initValues(1000,0) == 1000
    assert ampcountpy.initValues(1,1) == 1
    assert ampcountpy.initValues(10,1) == 19
    assert ampcountpy.initValues(1000,1) == 1999

def test_generateAmplificationTable():
    x=ampcountpy.generateAmplificationTable(5,5)
    assert x[3][3] == 19
    assert x[3][0] == 3
    assert x[0][3] == 0
    assert x[2][2] == 5
    x=ampcountpy.generateAmplificationTable(50,50)
    assert x[3][3] == 19
    assert x[3][0] == 3
    assert x[0][3] == 0
    assert x[2][2] == 5

def test_cumsum():
    assert [x for x in ampcountpy.cumsum([1,2,3])][2]==6
    assert [x for x in ampcountpy.cumsum([1,2,3,4,5,6])][2]==6
    assert [x for x in ampcountpy.cumsum([1,1,1,1,1,1,10,100])][6]==16
    assert [x for x in ampcountpy.cumsum([1,1,1,1,1,-5,10,100])][6]==10
    cs=ampcountpy.cumsum([2]*100)
    counter=2
    for x in cs:
        assert x == counter
        counter+=2


def test_countAmplifications():
    assert ampcountpy.countAmplifications(3,3) == 19
    assert ampcountpy.countAmplifications(3,0) == 3
    assert ampcountpy.countAmplifications(0,3) == 0
    assert ampcountpy.countAmplifications(2,2) == 5
