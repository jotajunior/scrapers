from flask import Flask
from flask.ext.cache import Cache
from bfhl.src import bfhl
from wow.src import wow
from riot.src import riot
import config

app = Flask(__name__)

cache = Cache(app,config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

@app.route('/bfhl/exists/<name>')
@cache.cached(timeout=1440)
def bfhl_exists(name):
    platform = 'pc'
    output = 'json'

    bf = bfhl.BFHL(platform)
    return str(bf.user_exists(name))

@app.route('/riot/exists/<name>/<region>')
@cache.cached(timeout=1440)
def riot_exists(name, region):
    r = riot.Riot(config.RIOT_API_KEY, region)
    
    return str(r.user_exists_by_name(name))

@app.route('/wow/user/<name>/<world>')
@cache.cached(timeout=1440)
def wow_user(name, world):
    w = wow.Wow()
    return str(w.get_user_info(name, world))

if __name__ == '__main__':
    app.run(debug=True)

