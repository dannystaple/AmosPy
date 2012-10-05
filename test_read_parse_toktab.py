__author__ = 'stapled'

from read_parse_toktab import process_similar
from nose.tools import assert_equals
from unittest import TestCase

def test_process_similar():
    pairs = [
        ('458', '"!ad","d"+$80,"I",-2', ('458+4 TkAd2:\tdc.w CAdd2-Tk,Synt-Tk', '+6 \tdc.b "!ad","d"+$80,"I",-2')),
        ('462', '$80,"I",-1', ('462+4 TkAd4:\tdc.w CAdd4-Tk,Synt-Tk', '+4 \tdc.b $80,"I",-1'))
    ]
    out = list(process_similar(pairs))
    expected = '"ad","d"+$80,"I",-2'
    assert_equals(out[1][1], '"ad","d"+$80,"I",-2')

