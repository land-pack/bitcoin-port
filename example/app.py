import traceback
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

@app.route("/api/tx/createrawtransaction", methods=['POST'])
def api_tx_createrawtransaction():
    body = request.get_json(force=True)
    txid = body.get('txid')
    vout = body.get('vout')
    amount = body.get('amount')
    address = body.get('address')
    d = rpc_connection.createrawtransaction([{"txid":txid, "vout":vout}], {address: amount}) # 256 absurdly-high-fee
    return render_json(d)

@app.route("/api/tx/signrawtransaction", methods=['POST'])
def api_tx_signrawtransaction():
    """
	{
	  "txid":"ab9d02994fbca2f577c8deaa224e82dbfa3b3c5ecf3d3f0fd63aaff1c4f3c28c",
	  "vout":1,
	  "amount":0.8,
	  "address":"2MwkxLxbgdZKGEN4fS8GQATqQGXyRpFbkuf",
	  "scriptPubKey": "a914317fec65edbff6e4350fbe668cfedaf54ea9061587",
	  "redeemScript": "0014c21bbdc4a642e391a6401bf30ac3e4e8e9669ea2"
	}
    """
    body = request.get_json(force=True)
    txid = body.get('txid')
    vout = body.get('vout')
    amount = body.get('amount')
    address = body.get('address')
    scriptPubKey = body.get('scriptPubKey')
    redeemScript = body.get('redeemScript')
    sighashtype = body.get('sighashtype') if body.get('sighashtype') else 'ALL'
    dumpprivkey = body.get('dumpprivkey') if body.get('dumpprivkey') else rpc_connection.dumpprivkey(address)
    raw_tx_hex = body.get('raw_tx_hex') if body.get('raw_tx_hex') else rpc_connection.createrawtransaction(
            [{"txid":txid, "vout":vout}], {address: amount}) # 256 absurdly-high-fee
    d = rpc_connection.signrawtransaction(raw_tx_hex, [{"txid":txid, "vout":vout, "scriptPubKey":scriptPubKey, 
            "redeemScript":redeemScript}], [dumpprivkey], sighashtype) # 256 absurdly-high-fee
    return render_json(d)

@app.route("/api/v1/tx/sendrawtransaction", methods=['POST'])
def api_tx_sendrawtransaction():
    """
	{
	  "txid":"ab9d02994fbca2f577c8deaa224e82dbfa3b3c5ecf3d3f0fd63aaff1c4f3c28c",
	  "vout":1,
	  "amount":0.8,
	  "address":"2MwkxLxbgdZKGEN4fS8GQATqQGXyRpFbkuf",
	  "scriptPubKey": "a914317fec65edbff6e4350fbe668cfedaf54ea9061587",
	  "redeemScript": "0014c21bbdc4a642e391a6401bf30ac3e4e8e9669ea2"
	}
    """
    body = request.get_json(force=True)
    txid = body.get('txid')
    vout = body.get('vout')
    amount = body.get('amount')
    address = body.get('address')
    scriptPubKey = body.get('scriptPubKey')
    redeemScript = body.get('redeemScript')
    dumpprivkey = body.get('dumpprivkey') if body.get('dumpprivkey') else rpc_connection.dumpprivkey(address)
    raw_tx_hex = body.get('raw_tx_hex') if body.get('raw_tx_hex') else rpc_connection.createrawtransaction(
            [{"txid":txid, "vout":vout}], {address: amount}) # 256 absurdly-high-fee
    hex_object = rpc_connection.signrawtransaction(raw_tx_hex, [{"txid":txid, "vout":vout, "scriptPubKey":scriptPubKey, 
            "redeemScript":redeemScript}], [dumpprivkey]) # 256 absurdly-high-fee
    hex_code = hex_object.get("hex")
    try:
        d = rpc_connection.sendrawtransaction(hex_code)
    except:
        d = {
            "traceback": traceback.format_exc()
        }
    return render_json(d)




@app.route("/api/v2/tx/sendrawtransaction", methods=['POST'])
def api_tx_sendrawtransaction_safe():
    """
	{
	  "txid":"ab9d02994fbca2f577c8deaa224e82dbfa3b3c5ecf3d3f0fd63aaff1c4f3c28c",
	  "vout":1,
	  "amount":0.8,
	  "address":"2MwkxLxbgdZKGEN4fS8GQATqQGXyRpFbkuf",
	  "scriptPubKey": "a914317fec65edbff6e4350fbe668cfedaf54ea9061587",
	  "redeemScript": "0014c21bbdc4a642e391a6401bf30ac3e4e8e9669ea2"
	}
    """
    body = request.get_json(force=True)
    txid = body.get('txid')
    vout = body.get('vout')
    amount = body.get('amount')
    address = body.get('address')
    scriptPubKey = body.get('scriptPubKey')
    redeemScript = body.get('redeemScript')
    dumpprivkey = body.get('dumpprivkey') if body.get('dumpprivkey') else rpc_connection.dumpprivkey(address)
    raw_tx_hex = body.get('raw_tx_hex') if body.get('raw_tx_hex') else rpc_connection.createrawtransaction(
            [{"txid":txid, "vout":vout}], {address: amount}) # 256 absurdly-high-fee
            #[{"txid":txid, "vout":vout}], {address: amount, address2: amount of rest balance}) # 256 absurdly-high-fee
            
    hex_object = rpc_connection.signrawtransaction(raw_tx_hex, [{"txid":txid, "vout":vout, "scriptPubKey":scriptPubKey, 
            "redeemScript":redeemScript, "amount":amount}], [dumpprivkey]) # 256 absurdly-high-fee
    hex_code = hex_object.get("hex")
    try:
        d = rpc_connection.sendrawtransaction(hex_code)
    except:
        d = {
            "traceback": traceback.format_exc()
        }
    return render_json(d)


@app.route("/api/v3/tx/sendrawtransaction", methods=['POST'])
def api_tx_v3_sendrawtransaction_safe():
    """
	{
	  "txid":"ab9d02994fbca2f577c8deaa224e82dbfa3b3c5ecf3d3f0fd63aaff1c4f3c28c",
	  "vout":1,
	  "amount":0.8,
	  "address":"2MwkxLxbgdZKGEN4fS8GQATqQGXyRpFbkuf",
	  "scriptPubKey": "a914317fec65edbff6e4350fbe668cfedaf54ea9061587",
	  "redeemScript": "0014c21bbdc4a642e391a6401bf30ac3e4e8e9669ea2"
	}
    """
    body = request.get_json(force=True)
    txid_generate_by = body.get('method') or 'sendfrom'

    txid = rpc_connection.sendfrom(fromaccount, toaddress, amount)
    vout = body.get('vout')
    amount = body.get('amount')
    address = body.get('address')
    scriptPubKey = body.get('scriptPubKey')
    redeemScript = body.get('redeemScript')

    dumpprivkey =  rpc_connection.dumpprivkey(address)
    raw_tx_hex = rpc_connection.createrawtransaction([{"txid":txid, "vout":vout}], {address: amount}) # 256 absurdly-high-fee
            
    hex_object = rpc_connection.signrawtransaction(raw_tx_hex, [{"txid":txid, "vout":vout, "scriptPubKey":scriptPubKey, 
            "redeemScript":redeemScript, "amount":amount}], [dumpprivkey]) # 256 absurdly-high-fee
    hex_code = hex_object.get("hex")
    try:
        d = rpc_connection.sendrawtransaction(hex_code)
    except:
        d = {
            "traceback": traceback.format_exc()
        }
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
@app.route("/api/tx/decoderawtransaction/<hex_code>")
def api_tx_decoderawtransaction(hex_code):
    d = rpc_connection.decoderawtransaction(hex_code)
    return render_json(d)

@app.route("/api/block-index/<block_index>")
def api_block_index(block_index):
    d = rpc_connection.getrawblock(block_index)
    return render_json(d)



if __name__ == '__main__':
    app.run(debug=True)
