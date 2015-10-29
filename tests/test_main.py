import pytest
import ampcountpy
from ampcountpy import __main__
import argparse
import os, stat
def test_check_positive_int():
    with pytest.raises(argparse.ArgumentTypeError):
        __main__.check_positive_int(-1)
    with pytest.raises(ValueError):
        __main__.check_positive_int("asdas")

def test_checkFile(tmpdir):
    d = tmpdir.mkdir('dir')
    p = d.join('test.txt')
    with pytest.raises(argparse.ArgumentTypeError):
        __main__.check_file(str(d))
    #doesn't exist yet
    with pytest.raises(argparse.ArgumentTypeError):
        __main__.check_file(str(p))
    p.write("test")
    assert __main__.check_file(str(p))==str(p)
    #make unreadable
    os.chmod(str(p),os.stat(str(p)).st_mode & ~stat.S_IREAD)
    with pytest.raises(argparse.ArgumentTypeError):
        __main__.check_file(str(p))

def test_readBindingSites(tmpdir):
    d = tmpdir.mkdir('dir')
    p = d.join('test.txt')
    p.write("1 10 20\n21 30")
    assert all([x==y for x,y in zip(__main__.readBindingSites(str(p)),[1, 10, 20, 21, 30])])

def test_main(capsys,tmpdir):
    with pytest.raises(SystemExit):
        __main__.main()
    out, err=capsys.readouterr()
    assert 'usage' in err
    with pytest.raises(SystemExit):
        __main__.main(['-h'])
    out, err=capsys.readouterr()
    assert 'usage' in out
    d = tmpdir.mkdir('dir')
    f = d.join('forward.txt')
    r = d.join('reverse.txt')
    o = d.join('output.txt')
    f.write("1 10 20")
    r.write("")
    __main__.main(['-f',str(f),'-r',str(r),'-o',str(o)])
    out=o.read().split('\n')[1:]
    amps=[int(x.split(',')[2]) for x in out if len(x)>0]
    assert all([x==y for x,y in zip(amps,[1,2,3,2,1])])
    r.write("30 42 51\n\n")
    __main__.main(['-f',str(f),'-r',str(r),'-o',str(o)])
    out=o.read().split('\n')[1:]
    amps=[int(x.split(',')[2]) for x in out if len(x)>0]
    assert max(amps)==38
    #check start ends and max length
    __main__.main(['-f',str(f),'-r',str(r),'-o',str(o),'-l',str(100)])
    out=[x for x in o.read().split('\n')[1:] if len(x)>0]
    assert int(out[0].split(',')[0])==1
    assert int(out[-1].split(',')[1])==119
    #check max genome size
    __main__.main(['-f',str(f),'-r',str(r),'-o',str(o),'-l',str(100),'-g',str(60)])
    out=[x for x in o.read().split('\n')[1:] if len(x)>0]
    assert int(out[0].split(',')[0])==1
    assert int(out[-1].split(',')[1])==60
    amps=[int(x.split(',')[2]) for x in out if len(x)>0]
    assert max(amps)==38
    __main__.main(['-f',str(f),'-r',str(r),'-o',str(o),'-v'])
    out, err=capsys.readouterr()



def test_commandline(capsys,tmpdir):
    d = tmpdir.mkdir('dir')
    f = d.join('forward.txt')
    r = d.join('reverse.txt')
    o = d.join('output.txt')
    f.write("3 10 20 24 49")
    r.write("30 42 51 90\n\n")
    __main__.main(['-f',str(f),'-r',str(r),'-o',str(o)])
    o2 = d.join('output2.txt')
    os.system('ampcount -f '+str(f)+' -r '+str(r)+' -o '+str(o2))
    assert o.read() == o2.read()
    o3 = d.join('output3.txt')
    os.system('python -m ampcountpy -f '+str(f)+' -r '+str(r)+' -o '+str(o3))
    assert o.read() == o3.read()
