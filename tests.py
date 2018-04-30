from base64 import b64encode
import json
import time
from lambda_function import lambda_handler


if __name__ == '__main__':

    event = {
        'queryStringParameters': {
            'invocation': 'eyJncmFwaHFsX3F1ZXJ5IjogInF1ZXJ5KFxuICAgICRDQVIxX1NlcmllczpTdHJpbmcsIFxuICAgICRDQVIxX1RyYW5zbWlzc2lvbl9Ecml2ZVRyYWluOlN0cmluZ1xuICAgICl7XG4gICAgcHJpY2luZyhcbiAgICAgICAgc2VyaWVzOiAkQ0FSMV9TZXJpZXMsIFxuICAgICAgICB0cmFpbnNtaXNzaW9uX2RyaXZldHJhaW46ICRDQVIxX1RyYW5zbWlzc2lvbl9Ecml2ZVRyYWluXG4gICAgICAgICl7XG4gICAgICAgIHRyaW1cbiAgICAgICAgcm9sbGluZ1ByaWNlXG4gICAgfVxufSIsICJncmFwaHFsX3ZhcmlhYmxlcyI6IHsiQ0FSMV9UcmFuc21pc3Npb25fRHJpdmVUcmFpbiI6ICJhd2QiLCAiQ0FSMV9TZXJpZXMiOiAiY3gtNSJ9LCAiZXhwaXJlZF9pbiI6IDE1MjQzMDkxNDguNjcxNTczLCAiaW52b2NhdGlvbl9pZCI6ICJtajl6bWxwcXhoOTJ0eiJ9',
            'token': 'd279316c4787f9b41da8dc307dfc4414dec4426456e6a51c351ef5cce9dd6be9',
        }
    }

    result = lambda_handler(event, {}, pass_token=True)

    print(result)
