import json
from lambda_function import lambda_handler
from base64 import b64encode
import time


if __name__ == '__main__':

    event = {
        'queryStringParameters': {
              "invocation": "eyJncmFwaHFsX3F1ZXJ5IjogIiBxdWVyeSgkQ0FSX01BS0VSMTpTdHJpbmchKSB7XG4gICAgbWFrZXIgKGJyYW5kOiAkQ0FSX01BS0VSMSkge1xuICAgICAgICBicmFuZFxuICAgICAgICBuYW1lXG4gICAgICAgIGZvdW5kXG4gICAgICAgIGZvdW5kZXIge1xuICAgICAgICAgICAgbmFtZVxuICAgICAgICB9XG4gICAgICAgIG5hdGl2ZU5hbWVcbiAgICAgICAgZGVzY3JpcHRpb25cbiAgICAgICAgcmV2ZW51ZVxuICAgICAgICBuZXRJbmNvbWVcbiAgICAgICAgbG9nbyB7XG4gICAgICAgICAgICB1cmxcbiAgICAgICAgfVxuICAgICAgICBkaXZpc2lvbnMge1xuICAgICAgICAgICAgbmFtZVxuICAgICAgICB9XG4gICAgICAgIHNoYXJlaG9sZGVycyB7XG4gICAgICAgICAgICBuYW1lXG4gICAgICAgICAgICBzaGFyZVxuICAgICAgICB9XG4gICAgICAgIGltYWdlIHtcbiAgICAgICAgICAgIHVybFxuICAgICAgICAgICAgZGVzY3JpcHRpb25cbiAgICAgICAgfVxuICAgICAgICBzYWxlcyB7XG4gICAgICAgICAgICB5ZWFyXG4gICAgICAgICAgICB1bml0c1xuICAgICAgICAgICAgcmFua1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuIiwgImdyYXBocWxfdmFyaWFibGVzIjogeyJDQVJfTUFLRVIxIjogImF1ZGkifSwgImV4cGlyZWRfaW4iOiAxNTI2NDc1MTExLjUyODA2NiwgImludm9jYXRpb25faWQiOiAibnIxeWxrYjBqY3k0cGIifQ==",
              "token": "72c2afbf809d89e388d5e964bfd1dedbf102d094064fa57a65aba0a6c0291254"
                }
    }

    result = lambda_handler(event, {}, pass_token=True)

    print(result)
    print(json.dumps(json.loads(result['body'][7:-1]), indent=4))
