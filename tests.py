from base64 import b64encode
import json
import time
from lambda_function import lambda_handler


if __name__ == '__main__':

    query = '''
            query getMaker($car_maker:String!) {
            maker (brand: $car_maker) {
                brand
                name
                found
                revenue
                netIncome
                logo
                founder
                shareholders {
                    name
                    share
                }
                image {
                    url
                    description
                }
              }
            }
            '''

    # query = '''
    #         query getModel($name:String,$trim:String,$series:String,$maker:String) {
    #             model (name: $name,trim: $trim,series: $series,maker: $maker) {
    #                 series {
    #                     name
    #                     maker {
    #                         brand
    #                         name
    #                     }
    #                 }
    #               }
    #         }
    #         '''

    # https://yeg1enajha.execute-api.us-east-1.amazonaws.com/dev/otnskills?invocation=eyJpbnZvY2F0aW9uIjogeyJJbnZvY2F0aW9uIjogW3siRmluZCI6IFt7InRvIjogIkNBUl9NQUtFUiQxIn0sIHsib2JqZWN0cyI6IFt7IkFHRU5UIjogImFnZW50In0sIHsiQ0FSX01BS0VSJDEiOiAicHJpbWFyeSJ9XX0sICJldmVudHMiLCB7ImNvbmRpdGlvbnMiOiB7IiRsYW1iZGEiOiBbeyIkdmFycyI6ICJDQVJfTUFLRVIkMSJ9LCB7IiRhbmQiOiB7IiRlcSI6IFsiQ0FSX01BS0VSJDEiLCAiYXVkaSJdfX1dfX1dfSwgeyJlcnJvcnMiOiBudWxsfV19LCAianNfdHJhbnNmb3JtIjogbnVsbCwgImdyYXBocWxfdmFyaWFibGVzIjogeyJjYXJfbWFrZXIiOiAiYXVkaSJ9LCAiZXhwaXJlZF9pbiI6IDE1MjM1MjIyMTcuODA0NjYsICJncmFwaHFsX3F1ZXJ5IjogIiAgICAgICAgIHF1ZXJ5IGdldE1ha2VyKCRjYXJfbWFrZXI6U3RyaW5nISkge1xuICAgICAgICAgICAgbWFrZXIgKGJyYW5kOiAkY2FyX21ha2VyKSB7XG4gICAgICAgICAgICAgICAgYnJhbmRcbiAgICAgICAgICAgICAgICBuYW1lXG4gICAgICAgICAgICAgICAgZm91bmRcbiAgICAgICAgICAgICAgICByZXZlbnVlXG4gICAgICAgICAgICAgICAgbmV0SW5jb21lXG4gICAgICAgICAgICAgICAgbG9nb1xuICAgICAgICAgICAgICAgIGZvdW5kZXJcbiAgICAgICAgICAgICAgICBzaGFyZWhvbGRlcnMge1xuICAgICAgICAgICAgICAgICAgICBuYW1lXG4gICAgICAgICAgICAgICAgICAgIHNoYXJlXG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGltYWdlIHtcbiAgICAgICAgICAgICAgICAgICAgdXJsXG4gICAgICAgICAgICAgICAgICAgIGRlc2NyaXB0aW9uXG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4ifQ==&token=0de69e6aabbde828ee1484e9cbe1c5f065b3dff78c7fd2e7997b00d96f13e688
    event = {
        'queryStringParameters': {
            'invocation': 'eyJqc190cmFuc2Zvcm0iOiBudWxsLCAiZ3JhcGhxbF92YXJpYWJsZXMiOiB7IkNBUl9NQUtFUl8xIjogImF1ZGkifSwgImV4cGlyZWRfaW4iOiAxNTIzNTM2Mjc2LjcxMjgzNywgImdyYXBocWxfcXVlcnkiOiAiICAgICAgICAgcXVlcnkgZ2V0TWFrZXIoJENBUl9NQUtFUl8xOlN0cmluZyEpIHtcbiAgICAgICAgICAgIG1ha2VyIChicmFuZDogJENBUl9NQUtFUl8xKSB7XG4gICAgICAgICAgICAgICAgYnJhbmRcbiAgICAgICAgICAgICAgICBuYW1lXG4gICAgICAgICAgICAgICAgZGVzY3JpcHRpb25cbiAgICAgICAgICAgICAgICBmb3VuZFxuICAgICAgICAgICAgICAgIHJldmVudWVcbiAgICAgICAgICAgICAgICBuZXRJbmNvbWVcbiAgICAgICAgICAgICAgICBsb2dvXG4gICAgICAgICAgICAgICAgZm91bmRlclxuICAgICAgICAgICAgICAgIHNoYXJlaG9sZGVycyB7XG4gICAgICAgICAgICAgICAgICAgIG5hbWVcbiAgICAgICAgICAgICAgICAgICAgc2hhcmVcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgaW1hZ2Uge1xuICAgICAgICAgICAgICAgICAgICB1cmxcbiAgICAgICAgICAgICAgICAgICAgZGVzY3JpcHRpb25cbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiJ9',
            'token': 'e5fd3010d7e452371a58747abf77f42bc937e1e7c82b84d249a8745aa12bf23c',
        }
    }

    result = lambda_handler(event, {}, pass_token=True)

    print(result)
