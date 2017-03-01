def load_src(name, fpath):
    import os, imp
    p = fpath if os.path.isabs(fpath) \
        else os.path.join(os.path.dirname(__file__), fpath)
    return imp.load_source(name, p)

load_src('Splitter', "../Splitter.py")
from Splitter import *


def test_empty():
    string = ''

    constanted = detect_const(string)
    splitted = imp_split(string)

    assert constanted == '' and\
           splitted == []


def test_func_example():
    string =\
        'def func(a, b):\n'\
        '    for line in a:\n'\
        '        print line, \'abc\', "dsfs", b\n'\
        '    return 0'

    constanted = detect_const(string)
    splitted = imp_split(constanted)

    assert constanted ==\
        'def func(a, b):\n'\
        '    for line in a:\n'\
        '        print line, _CONST, _CONST, b\n'\
        '    return _CONST' and \
        splitted == ['def', 'func', '(', 'a', ',', 'b', ')', ':', 'for', 'line', 'in', 'a', ':', 'print', 'line',
                     ',', '_CONST', ',', '_CONST', ',', 'b', 'return', '_CONST']


def test_const_detection():
    string = '1234 1.23 [a, b] {1:1} [{1: 1}, {2: 2}] {1: [1, 1]} \'ab\' "ab" \'123\' "123" \'"ab"\' "\'ab\'" """aaa"""'

    constanted = detect_const(string)
    splitted = imp_split(constanted)

    assert constanted == '_CONST _CONST _CONST _CONST _CONST _CONST _CONST _CONST _CONST _CONST _CONST _CONST _CONST' and \
           splitted == ['_CONST', '_CONST', '_CONST', '_CONST', '_CONST', '_CONST', '_CONST',
                        '_CONST', '_CONST', '_CONST', '_CONST', '_CONST', '_CONST']