import falcon
from fastcnn.util import Fastcnn

api = application = falcon.API()
Fastcnn = Fastcnn()
api.add_route('/fastcnn', Fastcnn)