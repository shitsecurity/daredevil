#!/usr/bin/env python

import requests.packages
requests.packages.urllib3.disable_warnings()

from requests import Session as RequestsSession

class Session( RequestsSession ):

    UA = 'Mozilla/5.0'

    def __init__( self, cookies={}, *args, **kwargs ):
        super( Session, self ).__init__( *args, **kwargs )
        self.set_cookies(cookies)
        self.headers['User-Agent'] = Session.UA

    def set_cookies(self, cookies):
        for k,v in cookies.iteritems():
            self.cookies[k]=v

def get(ctx, injection):
    return fetch(ctx.session,'get',ctx.target.format(injection))

def post(ctx, injection):
    return fetch(ctx.session,'post',ctx.target,data=ctx.data.format(injection))

def fetch(session, method, url, headers={}, cookies={}, data=None):
    return session.request(method=method,
                           url=url,
                           headers=headers,
                           cookies=cookies,
                           data=data,
                           timeout=30,
                           verify=False,
                           allow_redirects=True)
