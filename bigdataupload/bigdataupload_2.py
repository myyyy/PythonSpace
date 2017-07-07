#!/usr/bin/env python3
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url, stream_request_body
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from post_streamer import PostDataStreamer
import sys

class MyPostDataStreamer(PostDataStreamer):
    percent = 0

    def on_progress(self):
        """Override this function to handle progress of receiving data."""
        if self.total:
            new_percent = self.received*100//self.total
            if new_percent != self.percent:
                self.percent = new_percent
                print("progress",new_percent)

@stream_request_body 
class StreamHandler(RequestHandler):
    def get(self):
        self.write('''<html><body>
<form method="POST" action="/" enctype="multipart/form-data">
File #1: <input name="file1" type="file"><br>
File #2: <input name="file2" type="file"><br>
File #3: <input name="file3" type="file"><br>
Other field 1: <input name="other1" type="text"><br>
Other field 2: <input name="other2" type="text"><br>
Other field 3: <input name="other3" type="text"><br>
<input type="submit">
</form>
</body></html>''')

    def post(self):
        try:
            #self.fout.close()
            self.ps.finish_receive()
            # Use parts here!
            self.set_header("Content-Type","text/plain")
            oout = sys.stdout
            try:
                sys.stdout = self
                self.ps.examine()
            finally:
                sys.stdout = oout
        finally:
            # Don't forget to release temporary files.
            self.ps.release_parts()

    def prepare(self):
        # TODO: get content length here?
        try:
            total = int(self.request.headers.get("Content-Length","0"))
        except:
            total = 0
        self.ps = MyPostDataStreamer(total) #,tmpdir="/tmp"
        #self.fout = open("raw_received.dat","wb+")

    def data_received(self, chunk):
        #self.fout.write(chunk)
        # import pdb;pdb.set_trace()
        self.ps.receive(chunk)

def main():
    application = Application([
        url(r"/", StreamHandler),
    ])
    max_buffer_size = 4 * 1024**3 # 4GB
    http_server = HTTPServer(
        application,
        max_buffer_size=max_buffer_size,
    )
    http_server.listen(1994)
    IOLoop.instance().start()

main()