from flask import Flask, jsonify, request
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


def render_json(d):
    d=sjson.dumps(d, use_decimal=True)
    d = json.loads(d)
    return jsonify(d)



@app.route("/api/block/<block_id>")
def api_block(block_id):
    d = rpc_connection.getblock(block_id)
    return render_json(d)

# Transaction
@app.route("/api/tx/<tx>")
def api_tx_check(tx):
    # 5bc975913e48f64934a3e382a48569a7574b336014a5e1707d7683223d4f40ad
    d = rpc_connection.gettransaction(tx)
    return render_json(d)

@app.route("/api/account/<name>/balance")
def api_account_balance(name):
    d = rpc_connection.getbalance(name)
    return render_json(d)

@app.route("/api/account/<name>/balance")
def api_account_balance(name):
    d = rpc_connection.getbalance(name)
    return render_json(d)


@app.route("/api/getmininginfo")
def api_getmininginfo():
    return render_json(d)

@app.route("/api/listreceivedbyaddress")
def api_listreceivedbyaddress():
    d = rpc_connection.listreceivedbyaddress()
    return render_json(d)

@app.route("/api/validateaddress/<address>")
def api_validateaddress(address):
    d = rpc_connection.validateaddress(address)
    return render_json(d)

@app.route("/api/tx")
def api_tx_sendtoaddress():
    addr = request.args.get('addr')
    amount = request.args.get('amount')
    # Also store the request to mysql ...
    d = rpc_connection.sendtoaddress(addr, amount)
    return render_json(d)


@app.route("/api/status")
def api_status():
    """
    ?q=getInfo
    """
    q = request.args.get('q', 'default')
    q_to_functions = {
        'getdifficulty': rpc_connection.getdifficulty,
        'getblockcount': rpc_connection.getblockcount,
        'getmininginfo': rpc_connection.getmininginfo,
        'getbestblockhash': rpc_connection.getbestblockhash,
        'default': lambda : '{"status": "invalid function"}'
    }
    d = q_to_functions.get(q, 'default')()
    return render_json(d)

#  Rest Of Api
@app.route("/api/rawblock/<block_id>")
def api_rawblock(block_id):
    d = rpc_connection.getrawblock(block_id)
    return render_json(d)

@app.route("/api/block-index/<block_index>")
def api_block_index(block_index):
    d = rpc_connection.getrawblock(block_index)
    return render_json(d)



if __name__ == '__main__':
    app.run(debug=True)
