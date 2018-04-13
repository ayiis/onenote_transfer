#coding=utf8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import re, datetime, json, time, traceback
import tornado
from tornado import (gen, httpserver, ioloop, web, httpclient)

from tornado.options import define, options
define("port", default=19999)

async_client = tornado.httpclient.AsyncHTTPClient(max_clients=100)
construct_url = "http://192.168.32.222:19999/mss?"

class defaultHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        try:
            self.request.headers["host"] = re.match('http(s)?://([^/ \"]*)/.*', self.request.query).groups()[1]
            self.request.headers["referer"] = ""
            request_options = httpclient.HTTPRequest(url=self.request.query, method="GET", headers=self.request.headers)
            result = yield async_client.fetch(request_options, raise_error=False)
        except Exception as e:
            self.finish(traceback.format_exc())

        response = self.convert(result.body)
        self.finish(response)


    def convert_lazy_load(self, sub_result):
        text = sub_result.group()
        if " data-src=\"" in text:
            return text.replace(" src=\"", " nosrc=\"").replace(" data-src=\"", " src=\"")
        else:
            return text

    def convert(self, data):
        data = re.sub(r"(http(s)?://[^/ >]*/)", lambda sub_result: construct_url + str(sub_result.group(1)), data)
        data = re.sub(r"<img[^>]*>", lambda sub_result: self.convert_lazy_load(sub_result), data)

        return data


@gen.coroutine
def init():
    try:
        options.parse_command_line()

        settings = {
            "autoreload": True
        }
        app = web.Application([
            ("/mss", defaultHandler)
        ], **settings)
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port)

        print "init success:", options.port
    except:
        print traceback.format_exc()


if __name__ == "__main__":
    init()
    ioloop.IOLoop.current().start()
