
from fparser import api

def test_reproduce_issue():
    source_str = '''\
      subroutine bndfp()
      use m_struc_def
C-
C 
C
C
C
C
      end
'''
    tree = api.get_reader(source_str, isfree=False, isstrict=False)
    s, u, c, e = list(tree)
    assert s.span==(1,1),`s.span`
    assert u.span==(2,2),`u.span`
    assert c.span==(3,8),`c.span`
    assert e.span==(9,9),`e.span`

def test_reproduce_issue_fix77():
    source_str = '''\
      subroutine foo()
      real a
c
c
      end
'''
    tree = api.get_reader(source_str, isfree=False, isstrict=True)
    foo, a, comment, end = list(tree)
    assert foo.span==(1,1)
    assert a.span==(2,2),`a.span`
    assert comment.span==(3,4)
    assert end.span==(5,5),`end.span`

def test_reproduce_issue_fix90():
    source_str = '''\
      subroutine foo()
      real a
c 1
c 2
      end
'''
    tree = api.get_reader(source_str, isfree=False, isstrict=False)
    foo, a, comment,end = list(tree)
    assert foo.span==(1,1)
    assert a.span==(2,2),`a.span`
    assert end.span==(5,5),`end.span`

    source_str = '''\
      subroutine foo()
      real a
c-
c
      end
'''
    tree = api.get_reader(source_str, isfree=False, isstrict=False)
    foo, a, comment,end = list(tree)
    assert foo.span==(1,1)
    assert a.span==(2,2),`a.span`
    assert end.span==(5,5),`end.span`

    source_str = '''\
      subroutine foo()
      real a
c
c
      end
'''
    tree = api.get_reader(source_str, isfree=False, isstrict=False)
    foo, a, comment, end = list(tree)
    assert foo.span==(1,1)
    assert a.span==(2,2),`a.span`
    assert comment.span == (3,4)
    assert end.span==(5,5),`end.span`

def test_comment_cont_fix90():
    source_str = '''\
          subroutine foo()
      real
c 1
     & a
c 2
      end
'''
    tree = api.get_reader(source_str, isfree=False, isstrict=False)
    foo, a, comment, end = list(tree)
    assert foo.span==(1,1)
    assert a.span==(2,4),`a.span`
    assert comment.span==(3,5),`comment.span`
    assert end.span==(6,6)

    source_str = '''\
          subroutine foo()
      real
c
     & a
c 2
      end
'''
    tree = api.get_reader(source_str, isfree=False, isstrict=False)
    foo, a, comment, end = list(tree)
    assert foo.span==(1,1)
    assert a.span==(2,4),`a.span`
    assert comment.span==(3,5),`comment.span`
    assert end.span==(6,6)

    source_str = '''\
          subroutine foo()
      real
c 1
     & a
c
      end
'''
    tree = api.get_reader(source_str, isfree=False, isstrict=False)
    foo, a, comment, end = list(tree)
    assert foo.span==(1,1)
    assert a.span==(2,4),`a.span`
    assert comment.span==(3,5),`comment.span`
    assert end.span==(6,6)

    source_str = '''\
          subroutine foo()
      real
c 1
     & a
c 2
     &,b
      end
'''
    tree = api.get_reader(source_str, isfree=False, isstrict=False)
    foo, ab, comment, end = list(tree)
    assert foo.span==(1,1)
    assert ab.span==(2,6),`a.span`
    assert comment.span==(3,5),`comment.span`
    assert end.span==(7,7)
