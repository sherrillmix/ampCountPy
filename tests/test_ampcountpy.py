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

def test_amplificationTable():
    assert len(ampcountpy.ampcount._AMPLIFICATIONTABLE) == ampcountpy.ampcount._MAXLOOKUP+1
    assert ampcountpy.ampcount._AMPLIFICATIONTABLE[0][0] == 0
    assert ampcountpy.ampcount._AMPLIFICATIONTABLE[0][1] == 0
    assert sum(ampcountpy.ampcount._AMPLIFICATIONTABLE[0]) == 0
    assert sum(ampcountpy.ampcount._AMPLIFICATIONTABLE[1]) == ampcountpy.ampcount._MAXLOOKUP+1
    assert ampcountpy.ampcount._AMPLIFICATIONTABLE[2][2] == 5
    assert ampcountpy.ampcount._AMPLIFICATIONTABLE[3][3] == 19

def test_cumsum():
    assert all([x==y for x,y in zip(ampcountpy.cumsum([1,2,3]),[1,3,6])])
    assert all([x==y for x,y in zip(ampcountpy.cumsum([1,2,3,4,5,6]),[1,3,6,10,15,21])])
    assert all([x==y for x,y in zip(ampcountpy.cumsum([1,1,1,1,1,1,10,100]),[1,2,3,4,5,6,16,116])])
    assert all([x==y for x,y in zip(ampcountpy.cumsum([1,-1,1,-1,1,-1,10,-100]),[1,0,1,0,1,0,10,-90])])
    assert all([x==y for x,y in zip(ampcountpy.cumsum([1]*100),range(1,101))])
    assert all([x==y for x,y in zip(ampcountpy.cumsum([2]*100),range(2,202,2))])


def test_countAmplifications():
    assert ampcountpy.countAmplifications(0,3) == 0
    assert ampcountpy.countAmplifications(0,9) == 0
    assert ampcountpy.countAmplifications(1,1) == 1
    assert ampcountpy.countAmplifications(1,9) == 1
    assert ampcountpy.countAmplifications(1,0) == 1
    assert ampcountpy.countAmplifications(9,0) == 9
    assert ampcountpy.countAmplifications(3,3) == 19
    assert ampcountpy.countAmplifications(2,2) == 5
    with pytest.raises(IndexError):
        ampcountpy.countAmplifications(ampcountpy.ampcount._MAXLOOKUP+1,0)
    with pytest.raises(IndexError):
        ampcountpy.countAmplifications(0,ampcountpy.ampcount._MAXLOOKUP+1)
    with pytest.raises(IndexError):
        ampcountpy.countAmplifications(ampcountpy.ampcount._MAXLOOKUP+1,ampcountpy.ampcount._MAXLOOKUP+1)


def test_predictAmplications():
    assert max([x[2] for x in ampcountpy.predictAmplifications([1,2,3],[4,5,6])]) == 38
    assert len(ampcountpy.predictAmplifications([1,2,3],[4,5,6],10)) == 10

'''
test_that("Test predictAmplifications",{
	expect_that(max(predictAmplifications(1:3,4:6)$amplification), equals(38))
	expect_that(nrow(predictAmplifications(1:3,4:6,10)), equals(8))
	expect_that(nrow(predictAmplifications(1,c())), equals(1))
	expect_that(nrow(predictAmplifications(c(),1)), equals(1))
	expect_that(nrow(predictAmplifications(1:100,c())), equals(199))
	expect_that(nrow(predictAmplifications(c(),1e6+1:100,100)), equals(199))
	expect_that(max(predictAmplifications(c(),1)$amplification), equals(1))
	expect_that(max(predictAmplifications(1,c())$amplification), equals(1))
	expect_that(max(predictAmplifications(c(),1:100)$amplification), equals(100))
	expect_that(max(predictAmplifications(1:100,c())$amplification), equals(100))
	expect_that(max(predictAmplifications(1:500,c())$amplification), throws_error("limited to"))
	expect_that(max(predictAmplifications(c(),1:500)$amplification), throws_error("limited to"))
})
'''
