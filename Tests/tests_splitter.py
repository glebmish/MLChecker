from Splitter import *


def test_empty():
    string = ''
    splitted = imp_split(delimiters, string, detached)
    constanted = detect_const(splitted)
    assert splitted == [] and constanted == []

def test_func_example():
    string = \
    'def func(a, b):\n' \
      'for line in a:\n' \
        'print line, \'abc\', "dsfs", b\n' \
        'return 0'
    splitted = imp_split(delimiters, string, detached)
    constanted = detect_const(splitted)
    assert splitted == ['def', 'func', '(', 'a', ',', 'b', ')', ':', 'for', 'line', 'in', 'a', ':', 'print', 'line',
                        ',', "'", 'abc', "'", ',', '"', 'dsfs', '"', ',', 'b', 'return', '0'] and \
        constanted == ['def', 'func', '(', 'a', ',', 'b', ')', ':', 'for', 'line', 'in', 'a', ':', 'print', 'line',
                       ',', 'const', ',', 'const', ',', 'b', 'return', 'const']

def test_dif_splits_detaches():
    string = 'a simple string to check delimiters and detaches'
    delimiters = 'aie'
    detached = 'spd'
    splitted = imp_split(delimiters, string, detached)
    constanted = detect_const(splitted)
    assert splitted == [' ', 's', 'm', 'p', 'l', ' ', 's', 'tr', 'ng to ch', 'ck ', 'd', 'l', 'm', 't', 'r', 's',
                        ' ', 'n', 'd', ' ', 'd', 't', 'ch', 's'] and \
        constanted == [' ', 's', 'm', 'p', 'l', ' ', 's', 'tr', 'ng to ch', 'ck ', 'd', 'l', 'm', 't', 'r', 's',
                       ' ', 'n', 'd', ' ', 'd', 't', 'ch', 's']

def test_const_detection():
    string = '1234 1.23 [a, b] {a, b} \'ab\' "ab" \'123\' "123"'
    splitted = imp_split(delimiters, string, detached)
    constanted = detect_const(splitted)
    assert splitted == ['1234', '1.23', '[', 'a', ',', 'b', ']', '{', 'a', ',', 'b', '}', "'", 'ab', "'", '"', 'ab',
                        '"', "'", '123', "'", '"', '123', '"'] and \
        constanted == ['const', 'const', 'const', 'const', 'const', 'const', 'const', 'const']