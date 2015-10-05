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
    assert len(ampcountpy.predictAmplifications([1,2,3],[4,5,6],3)) == 6
    assert len(ampcountpy.predictAmplifications([1,2,3],[4,5,6],10)) == 8
    assert len(ampcountpy.predictAmplifications([1],[3],3)) == 1
    assert len(ampcountpy.predictAmplifications([1],[])) == 1
    assert len(ampcountpy.predictAmplifications([],[1])) == 1
    assert len(ampcountpy.predictAmplifications(range(1,101,1),[])) == 199
    assert len(ampcountpy.predictAmplifications([x+1e6 for x in range(1,101,1)],[])) == 199
    assert ampcountpy.predictAmplifications([1],[])[0][2] == 1
    assert ampcountpy.predictAmplifications([],[1])[0][2] == 1
    assert ampcountpy.predictAmplifications([1],[3],3)[0][2] == 2
    assert all([x[2]==y for x,y in zip(ampcountpy.predictAmplifications([1,3],[3],3),[2,4,1])])
    assert all([x[2]==y for x,y in zip(ampcountpy.predictAmplifications([1,3],[3,5],3),[2,10,2])])
    assert all([x[0]==y for x,y in zip(ampcountpy.predictAmplifications([1,3],[3,5],3),[1,3,4])])
    assert all([x[1]==y for x,y in zip(ampcountpy.predictAmplifications([1,3],[3,5],3),[2,3,5])])
    with pytest.raises(IndexError):
        ampcountpy.predictAmplifications(range(ampcountpy.ampcount._MAXLOOKUP+1),[0])
    with pytest.raises(IndexError):
        ampcountpy.predictAmplifications([0],range(ampcountpy.ampcount._MAXLOOKUP+1))

def test_predictAmplicationsSingleStrand():
    assert max([x[2] for x in ampcountpy.predictAmplificationsSingleStrand([1,2,3],[4,5,6])]) == 19
    assert len(ampcountpy.predictAmplificationsSingleStrand([1,2,3],[4,5,6],3)) == 6
    assert len(ampcountpy.predictAmplificationsSingleStrand([1,2,3],[4,5,6],10)) == 8
    assert len(ampcountpy.predictAmplificationsSingleStrand([1],[3],3)) == 2
    assert len(ampcountpy.predictAmplificationsSingleStrand([1],[])) == 1
    assert len(ampcountpy.predictAmplificationsSingleStrand([],[1])) == 1
    assert len(ampcountpy.predictAmplificationsSingleStrand(range(1,101,1),[])) == 199
    assert len(ampcountpy.predictAmplificationsSingleStrand([x+1e6 for x in range(1,101,1)],[])) == 199
    assert ampcountpy.predictAmplificationsSingleStrand([1],[])[0][2] == 1
    assert ampcountpy.predictAmplificationsSingleStrand([],[1])[0][2] == 0
    assert ampcountpy.predictAmplificationsSingleStrand([1],[3],3)[0][2] == 1
    assert all([x[2]==y for x,y in zip(ampcountpy.predictAmplificationsSingleStrand([1,3],[3],3),[1,3,1])])
    assert all([x[2]==y for x,y in zip(ampcountpy.predictAmplificationsSingleStrand([1,3],[3,5],3),[1,5,1])])
    assert all([x[0]==y for x,y in zip(ampcountpy.predictAmplificationsSingleStrand([1,3],[3,5],3),[1,3,4])])
    assert all([x[1]==y for x,y in zip(ampcountpy.predictAmplificationsSingleStrand([1,3],[3,5],3),[2,3,5])])
    with pytest.raises(IndexError):
        ampcountpy.predictAmplificationsSingleStrand(range(ampcountpy.ampcount._MAXLOOKUP+1),[0])
    with pytest.raises(IndexError):
        ampcountpy.predictAmplificationsSingleStrand([0],range(ampcountpy.ampcount._MAXLOOKUP+1))
    with pytest.raises(IndexError):
        ampcountpy.predictAmplificationsSingleStrand(range(ampcountpy.ampcount._MAXLOOKUP+1),range(ampcountpy.ampcount._MAXLOOKUP+1))


