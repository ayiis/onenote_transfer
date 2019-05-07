#coding=utf8
import re, datetime, json, time, traceback
import tornado
from tornado import (gen, httpserver, ioloop, web, httpclient)

from tornado.options import define, options
define("port", default=19999)

local_host = "127.0.0.1"
async_client = tornado.httpclient.AsyncHTTPClient(max_clients=100)
construct_url = "http://%s:19999/mss?" % local_host
# https://192.168.32.222:19999/mss?https://mp.weixin.qq.com/s?__biz=MzIxMzEzMjM5NQ==&mid=2651029560&idx=1&sn=437d90c61f84ea357c885dc8f94cea2b&chksm=8c4c553cbb3bdc2a0cdd2840e3d7ccfbecb62c83df3908f375bf587b0a0ed5504c73e55debe9&scene=38#wechat_redirect

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

        self.set_header("Content-Type", result.headers["Content-Type"])
        if "text/html" in result.headers["Content-Type"]:
            response = self.convert(result.body.decode("utf8"))
        else:
            response = result.body
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

        print("init success:", options.port)
        print("http://%s:19999/mss?xxxxxx" % local_host)
    except:
        print(traceback.format_exc())


if __name__ == "__main__":
    init()
    ioloop.IOLoop.current().start()
