#!/usr/bin/env python

import logging
import time

def boolean(pick, request, ctx, re):
    logging.info(ctx(pick))
    response = request(ctx, ctx(str(ord(pick))))
    return re(response.text)

def time(pick, request, ctx, threshold):
    logging.info(ctx(pick))
    start = time.time()
    response = request(ctx, ctx(str(ord(pick))))
    end = time.time()
    rtt = end-start
    return rtt > threshold # sleep on true
