#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from base64 import b64decode
import json
import hashlib
import hmac
import time
from skills_manager import GraphQLManager


client_secrets = {
    'nr1ylkb0jcy4pb': 'JdqCSvYC96Bz7jGS0NGABNTxEasx0IuI',
    'mj9zmlpqxh92tz': 'uLzFZXW0sqOUTiOxDVfycrR9CZ62MTt6',
    'u0ma9p6lmhejbf': 'wZe8fenKvzNfVsRNY8ERnCYdMPiZQ0Kj',
    'ghnwbonioo9nzc': 'VwpPXOf28XaPi8ZzRcLvnSeIjGFzoyGt',
    '9bmaeo13dq8zfm': 'SyMU3oislb8AB6toOAPV8SwoTvNe3f46',
    'pgnps9psbykzb1': 'vJkiKtQsh9slNjJdc5Yq9lEpAHE803oP',
}


graphql_manager = GraphQLManager()


def get_invocation(data, token, pass_token):

    invocation = json.loads(b64decode(data))
    client_secret = client_secrets.get(invocation.get('invocation_id'))

    secret_key = hashlib.new('sha256', client_secret).digest()
    hash = hmac.new(key=secret_key,
                    msg=data,
                    digestmod=hashlib.sha256).hexdigest()

    if not pass_token and hash != token:
        return False

    expired_in = invocation.get('expired_in')

    if expired_in < time.time():
        return False

    return invocation


def lambda_handler(event, context, pass_token=False):

    params = event.get('queryStringParameters')
    if not params:
        return {'statusCode': 400} # Bad Request

    data = params.get('invocation')
    token = params.get('token')

    invocation = get_invocation(data, token, pass_token)
    if not invocation:
        return {'statusCode': 403} # Forbidden

    json_string = json.dumps(graphql_manager.invoke(invocation))

    # return as a jsonp
    return {
        'statusCode': 200,
        'body': u'render(%s)' % json_string
    }

