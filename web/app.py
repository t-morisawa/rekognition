import responder

api = responder.API(cors=True, cors_params={
    'allow_origins': ['*'],
    'allow_methods': ['*'],
    'allow_headers': ['*'],
})

@api.route("/")
def hello_world(req, resp):
    resp.text = "hello, world!"
