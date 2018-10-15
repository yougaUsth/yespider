# coding = utf-8
import tornado.web
import tornado.ioloop


class LoginHandler(tornado.web.RequestHandler):
    def initialize(self):
        # name = self.get_argument("name","")
        template = self.get_template_namespace()
        pass

    def get(self):
        self.post()

    def post(self, *args, **kwargs):
        self.write("hello word")


def make_app():
    return tornado.web.Application([("/", LoginHandler)])


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    print "web server started"

    tornado.ioloop.IOLoop.current().start()
