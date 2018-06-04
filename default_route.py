# coding=utf8

# 第三方包
import tornado.gen
import tornado.httpclient
import tornado.web

import re, datetime, json, time, traceback

async_client = tornado.httpclient.AsyncHTTPClient(max_clients=100)

construct_url = "http://192.168.32.222:19999/go?aya="


class defaultHandler(tornado.web.RequestHandler):


    @tornado.gen.coroutine
    def get(self):
        print "======"
        print "In shoppingHandler get:", datetime.datetime.now()
        print "Uri:", self.request.uri
        print "Headers:", self.request.headers
        print "Query:", self.request.query

        if self.request.query[:3] != "aya":
            self.finish("or die")

        try:
            result = yield self.go_request(self.request.query[4:])
        except Exception as e:
            print traceback.format_exc()

        response = self.convert(result.body)
        self.finish(response)


    def go_request(self, url):

        self.request.headers["host"] = re.match('http(s)?://(.*)/.*', url).groups()[1]

        request_options = tornado.httpclient.HTTPRequest(
            url=url,
            method="GET",
            headers=self.request.headers,
            body=None,
            request_timeout=60,
            connect_timeout=60
        )

        return async_client.fetch(request_options, raise_error=False)


    def do_replace(self, sub_result):
        return construct_url + str(sub_result.group(1))


    def convert(self, response):
        return re.sub(r"(http(s)?://[^/ >]*/)", lambda sub_result: self.do_replace(sub_result), response)

