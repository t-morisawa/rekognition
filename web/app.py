import responder

api = responder.API()

@api.route("/")
def hello_world(req, resp):
    resp.text = "hello, world!"
