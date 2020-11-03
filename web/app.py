import responder

api = responder.API()

@api.route("/hello")
def hello_world(req, resp):
    resp.text = "hello, world!"
