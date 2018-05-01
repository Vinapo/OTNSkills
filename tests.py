import json
from lambda_function import lambda_handler
from base64 import b64encode
import time


if __name__ == '__main__':

    event = {
        'queryStringParameters': {
            'invocation': 'eyJncmFwaHFsX3F1ZXJ5IjogIiBxdWVyeSgkQ0FSX01BS0VSMTpTdHJpbmchKSB7XG4gICAgbWFrZXIgKGJyYW5kOiAkQ0FSX01BS0VSMSkge1xuICAgICAgICBicmFuZFxuICAgICAgICBuYW1lXG4gICAgICAgIGZvdW5kXG4gICAgICAgIGZvdW5kZXJcbiAgICAgICAgbmF0aXZlTmFtZVxuICAgICAgICBkZXNjcmlwdGlvblxuICAgICAgICByZXZlbnVlXG4gICAgICAgIG5ldEluY29tZVxuICAgICAgICBsb2dvIHtcbiAgICAgICAgICAgIHVybFxuICAgICAgICB9XG4gICAgICAgIGRpdmlzaW9uc1xuICAgICAgICBzaGFyZWhvbGRlcnMge1xuICAgICAgICAgICAgbmFtZVxuICAgICAgICAgICAgc2hhcmVcbiAgICAgICAgfVxuICAgICAgICBpbWFnZSB7XG4gICAgICAgICAgICB1cmxcbiAgICAgICAgICAgIGRlc2NyaXB0aW9uXG4gICAgICAgIH1cbiAgICAgICAgc2FsZXMge1xuICAgICAgICAgICAgeWVhclxuICAgICAgICAgICAgdW5pdHNcbiAgICAgICAgICAgIHJhbmtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiIsICJncmFwaHFsX3ZhcmlhYmxlcyI6IHsiQ0FSX01BS0VSMSI6ICJhdWRpIn0sICJleHBpcmVkX2luIjogMTUyNTE1NjY4My4wNTE4OTQsICJpbnZvY2F0aW9uX2lkIjogIm5yMXlsa2IwamN5NHBiIn0=',
            'token': 'bc2007977627a5435f36c97fbdb6b4e119b4f05e0d5af58a4d0edb2d19cc7d73',
        }
    }

    result = lambda_handler(event, {}, pass_token=True)

    print(result)
    print(json.dumps(json.loads(result['body'][7:-1]), indent=4))
