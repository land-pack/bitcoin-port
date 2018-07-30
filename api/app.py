from flask import Flask
from flask import jsonify
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


app = Flask(__name__)


"""
We are going to simulate a device, which can generate address,
public-key, private-key!
"""
# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_user = 'my_rpc'
rpc_password= 'my_rpc_password'
rpc_host = '192.168.1.86:9332'

rpc_connection = AuthServiceProxy("http://{}:{}@{}".format(rpc_user, rpc_password, rpc_host))


@app.route("/api/v1/newaddr")
def api_v1_new_addr():
    addr = rpc_connection.getnewaddress()
    pubkey_obj = rpc_connection.validateaddress(addr)
    pubkey = pubkey_obj.get("scriptPubKey")
    privkey = rpc_connection.dumpprivkey(addr)
    data = {
        "addr": addr,
        "pubkey": pubkey,
        "privkey": privkey
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)

