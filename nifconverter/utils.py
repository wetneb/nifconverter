# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import requests
from time import sleep

logger = logging.getLogger(__name__)

DBPEDIA_PREFIX = 'http://dbpedia.org/resource/'
DBPEDIA_PAGE_PREFIX = 'http://dbpedia.org/page/'
WIKIDATA_PREFIX = 'http://www.wikidata.org/entity/'

def retry_request(url, parameters=None, timeout=10, delay=10, retries=4):
    """
    Requests an URL with retries
    :returns: the Request object if succeeded
    """
    parameters = parameters or {}
    backoff = 2
    while retries:
        try:
            req = requests.get(url, parameters, timeout=timeout)
            if req.status_code != 404:
                req.raise_for_status()
            return req
        except requests.RequestException as e:
            logger.info('Retrying in {} seconds for {}'.format(delay, url))
            sleep(delay)
            retries -= 1
            delay *= backoff
            if not retries:
                raise


def get_redirect(url):
    """
    Checks if a URL redirects to another URL, in
    which case the new URL is returned. Otherwise None is returned.
    """
    # Sadly a HEAD request does not work for obscure encoding reasons...
    # See accompanying test case
    if not url.startswith('http'):
        return
    try:
        req = retry_request(url, delay=3, retries=1)
    except requests.exceptions.RequestException:
        return
    location = req.url
    if location and location != url:
        return location


def fetch_redirecting_uris(decoded_uris, mapped_uris):
    missing_dbps = set(decoded_uris) - set(mapped_uris)
    redirecting_uris = {}
    for missing_uri in missing_dbps:
        redirect = get_redirect(missing_uri.replace(DBPEDIA_PREFIX, DBPEDIA_PAGE_PREFIX))
        if redirect:
            redirecting_uris[missing_uri] = redirect

    return redirecting_uris



