#!/usr/bin/env python

import re

class Regex(object):

    def __init__(self, true=None, false=None):
        self.true = re.compile(true)
        self.false = re.compile(false)
        if true is None and false is None: raise ValueError()

    def __call__(self, data):
        if self.true is not None and self.true.search(data):
            return True
        elif self.false is not None and self.false.search(data):
            return False
        elif self.true is not None and self.false is None:
            return False
        elif self.false is not None and self.true is None:
            return True
