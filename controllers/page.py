import webapp2

class PageHandler(webapp2.RequestHandler):
    def get(self):

        self.response.out.write("hello world")


