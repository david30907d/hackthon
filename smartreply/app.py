import falcon
from smartreply.util import SmartReply

api = application = falcon.API()
smartreply = SmartReply()
api.add_route('/smartreply', smartreply)