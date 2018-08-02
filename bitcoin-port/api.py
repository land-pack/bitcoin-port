from flask import Flask
from flask import jsonify
from flask import request
from rpc import rpc_connection
app = Flask(__name__)

@app.route("/api/sendrawtransaction", methods=['POST'])
def send_raw_transaction():
    """
    0200000000010158afd105a01ae7e99b56f9f4f71781b6b16ae1930ac1e5b52fb55cb7902b700b0100000017160014f48d7e6ccc174de18db850b821b0358b46be7df2ffffffff032e66d9020000000017a91414f6b354529c0d4b9a61aa878e9825184ae825598700000000000000000e6a0c407275737469636269736f6e4662d9020000000017a914be9f78e08958c2131aee9ea1c8eef8ae0e9c999a8702473044022009937e18232282932bc4da7d2ffc63c48dd9e71b68e9ba9833e5aace1f50dd6302203f112dde466b1569683ad522fc04681116ae44697451bc1ab3568aced2fbde3b012102ff1db90e012cbe7306dd6fc4139ca12cfa9139ccf8d0457a616c67044cd6de3100000000
    """
    data = request.get_json(force=True)
    # print(data)
    tx_hex = data.get("hex")
    print(tx_hex)
    ret = rpc_connection.sendrawtransaction(tx_hex)
    return jsonify({"status": "ok", "message": ret})

if __name__ == '__main__':
    app.run(debug=True)
