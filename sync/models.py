import traceback
import mysql.connector


hostname = '192.168.1.86'
username = 'frank'
password = 'openmysql'
database = 'bitcoin'

conn = mysql.connector.connect( host=hostname, user=username, passwd=password, db=database)


class TransactionModel(object):
    def insert(self, txid, vout, address, redeemScript, scriptPubKey, amount,confirmations, spendable, solvable, safe, blockhash):
        try:
            cur = conn.cursor()
            sql = """INSERT INTO 
                t_tx(txid, vout, address, redeemScript, scriptPubKey,
                    amount, confirmations, spendable, solvable, safe, blockhash)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cur.execute(sql,(
                        txid, vout, address,redeemScript, 
                        scriptPubKey, amount, confirmations, 
                        spendable, solvable, safe, blockhash))
            conn.commit()
        except:
            conn.rollback()
            print(traceback.format_exc())

if __name__ == '__main__':
    tm = TransactionModel()
    tm.insert(
        "ca0c4f5c27abfc2a76c0ab0dc3f6c1dc845afe41dfb4ac9aa5fb80d960c007e7",
    	0,
    	"2MwmXBD451gf4RCR1uyVw4KjacrHWfAFkEX",
    	"00149ea2cef6d5c6b0af52d5ea9bb9dbec6412ae4c57",
    	"a914319b5481d69966644d3cf3c238be506d007ca8bf87",
    	37.99996240,
    	0,
    	"true",
    	"true",
    	"true",
        "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
  	)


	
	

