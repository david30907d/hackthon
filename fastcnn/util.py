from webargs import fields
from webargs.falconparser import parser, use_args
import requests, msgpack
import falcon, subprocess

class Fastcnn(object):
    argmap = {
        'img_url': fields.String(),
    }

    @use_args(argmap)
    def on_get(self, req, resp, args):
        img_url = args['img_url']
        response = requests.get(img_url, stream=True)

        with open('fastcnn.jpg', 'wb') as f:
            f.write(response.content)
        subprocess.call(['python', 'evaluate.py', '--checkpoint', '.', '--in-path', 'fastcnn.jpg', '--out-path', 'test'])
        resp.stream = open('test/fastcnn.jpg', 'rb')
        resp.content_type = falcon.MEDIA_MSGPACK
        resp.status = falcon.HTTP_200
