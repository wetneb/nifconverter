# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import requests
from time import sleep
logger = logging.getLogger(__name__)

def retry_request(url, parameters=None, timeout=10, delay=10):
    """
    Requests an URL with retries
    :returns: the Request object if succeeded
    """
    parameters = parameters or {}
    retries = 4
    backoff = 2
    while retries:
        try:
            req = requests.get(url, parameters, timeout=timeout)
            req.raise_for_status()
            return req
        except requests.RequestException as e:
            logger.info('Retrying in {} seconds for {}'.format(delay, url))
            sleep(delay)
            retries -= 1
            delay *= backoff
            if not retries:
                raise



