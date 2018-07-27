from bitcoinlib.wallets import HDWallet

w = HDWallet.create("wallet1")

print(w)


key1 = w.new_key()

print(key1)

print(key1.address)
