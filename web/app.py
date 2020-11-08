import responder
import reprlib
import aioboto3

api = responder.API(cors=True, cors_params={
    'allow_origins': ['*'],
    'allow_methods': ['*'],
    'allow_headers': ['*'],
})

@api.route("/")
async def hello_world(req, resp):

    data = await req.media(format='files')

    #f = open('./{}'.format(data['file']['filename']), 'w')
    #f.write(data['file']['content'].decode('utf-8'))
    #f.close()

    print(reprlib.repr(data))

    # resp.media = {'filename': str(data["image"]["filename"])}
    filename = []
    for v in data.values():
         filename.append({'filename': v["filename"]})

    resp.media = filename

    #print(data["image"])
    #resp.text = str(data["image"]["filename"])
