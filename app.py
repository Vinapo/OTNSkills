from wsgiref.simple_server import make_server
from lambda_function import lambda_handler


def app(environ, start_response):

    query_string = environ.get('QUERY_STRING')
    d = {}
    for v in query_string.split('&'):
        v = v.split('=', 1)
        d[v[0]] = v[1]

    event = {
        'queryStringParameters': d
    }

    result = lambda_handler(event, {})

    status = '200 OK' if result.get('statusCode') == 200 else '403 Forbidden'
    headers = [('Content-type', 'text/javascript')]

    start_response(status, headers)

    return result.get('body', '').encode("utf-8")


if __name__ == '__main__':
    port = 8101
    httpd = make_server('', port, app)
    print "Serving on port %s..." % port
    httpd.serve_forever()
