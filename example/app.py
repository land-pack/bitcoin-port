from flask import Flask, jsonify
import json
import simplejson as sjson
from pprint import pprint
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


app = Flask(__name__)

# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_user = 'my_rpc'
rpc_password= 'my_rpc_password'
rpc_host = '192.168.1.86:9332'
rpc_connection = AuthServiceProxy("http://{}:{}@{}".format(rpc_user, rpc_password, rpc_host))


    




@app.route("/api/block")
def api_block():

    d = rpc_connection.getblock('0000000000000000079c58e8b5bce4217f7515a74b170049398ed9b8428beb4a')
    d=sjson.dumps(d, use_decimal=True)
    d = json.loads(d)
    return jsonify(d)

if __name__ == '__main__':
    app.run(debug=True)
