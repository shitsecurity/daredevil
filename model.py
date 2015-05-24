#!/usr/bin/env python

from http import Session

class Context(object):

    def __init__(self, target, vector, query, data=None, session=None ):
        self.target = target
        self.vector = vector
        self.query = query

        self.session = session or Session()
        self.data = data

        self.index = None

    def __call__(self, search):
        return self.vector.format(inc=self.index,
                                  query=self.query,
                                  search=search)
