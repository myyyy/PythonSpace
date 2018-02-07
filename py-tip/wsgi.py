from wsgiref.simple_server import make_server

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return '<h1>Hello, web!</h1>'

httpd = make_server('', 8001, application)
print "Serving HTTP on port 8001..."
httpd.serve_forever()

