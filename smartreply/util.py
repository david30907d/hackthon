from webargs import fields
from webargs.falconparser import parser, use_args
import pickle, requests, json, random
from udicOpenData.stopwords import rmsw

class SmartReply(object):
    argmap = {
        'user_id': fields.Int(),
        'bearid': fields.String()
    }

    @use_args(argmap)
    def on_post(self, req, resp, args) -> None:
        user_id = args['user_id']
        bearid = args['bearid']
        replys = self.smart_reply(user_id, bearid)
        resp.body = json.dumps(replys, ensure_ascii=False)

    @staticmethod
    def smart_reply(user_id, bearid):
        user_profile = requests.get('https://www.dcard.tw/v2/friends/{}'.format(user_id), headers={
            'Authorization': 'Bearer {}'.format(bearid),
            'Content-Type': 'application/x-www-form-urlencoded'
        }).json()
        ontology = pickle.load(open('ontology.pkl', 'rb'))
        hashtags = pickle.load(open('hashtags.pkl', 'rb'))
        template = {
            'talent': [lambda x: '你喜歡{}喔！我也是誒😍😍😍'.format(x), lambda x: '你喜歡{}喔！下次約一下Ｒ😍'.format(x), lambda x: '我也喜歡{}喔，要不要一起？😍😍'.format(x)],
    #         'club': lambda x: '原來你參加過{}喔！'.format(x),
    #         'lecture': lambda x: '原來你對{}有興趣喔！'.format(x),
            'lovedCountry': [lambda x: '你有去過{}喔？有啥好玩的嗎？😊😊😊'.format(x), lambda x: '你有去過{}喔？可以看照片嗎？😊'.format(x), lambda x: '你也喜歡{}喔！要不要一起？'.format(x)],
            'trouble': [lambda x: '你有什麼{}的煩惱啊？我是個好聽眾喔😚😚😚'.format(x), lambda x: '你有什麼{}的煩惱啊？還好ㄇ😚'.format(x)],
    #         'wantToTry': lambda x: '要不要一起去{} XD'.format(x),
            'exchange':  [lambda x: '你很懂{}喔！可以教我嗎？😘 '.format(x), lambda x: '你很懂{}喔！好強喔😘 '.format(x),],
        }
        
        replys = []
        for key in template:
            for word in set(rmsw(user_profile[key])):
                if word in ontology and len(word) > 1 and word in hashtags:
                    replys.append(random.sample(template[key], 1)[0](word))
        if not replys:
            return ['以你的顏值，真的不用寫自介😘😘😘']
        return replys
