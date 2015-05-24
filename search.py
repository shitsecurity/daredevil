#!/usr/bin/env python

import string
import math
import logging

def binary(cmp, request, context, args=[], kwargs={}, alphabet=string.printable):
    alph = [ _ for _ in alphabet ]
    alph.sort()
    for i in range( int(math.log(len(alph),2))+1 ):
        split = len(alph)/2
        pick = alph[split]
        debug = '{step} {pick} {alph}'.format(step=i, pick=pick, alph=alph)
        if cmp(pick, request, context, *args, **kwargs):
            alph = alph[:split]
            dir = '<'
        else:
            alph = alph[-split-1:]
            dir = '>'
        logging.debug('{} {}'.format(dir, debug))
    return alph.pop()
