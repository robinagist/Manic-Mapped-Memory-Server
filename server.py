from utils.server import check_request
from manic.app import Manic
from utils.helpers import teapot
import config
from manic.blueprint import bp

'''
Manic - hella fast mapped memory lookup server
(c) 2018 - kaotik.io - All Rights Reserved

runs on top of Sanic async framework
'''

app = Manic()
app.blueprint(bp)

app.start(host=config.HOST, port=config.PORT)



