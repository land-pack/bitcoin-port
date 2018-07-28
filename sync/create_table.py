import traceback
import mysql.connector


hostname = '192.168.1.86'
username = 'frank'
password = 'openmysql'
database = 'bitcoin'

conn = mysql.connector.connect( host=hostname, user=username, passwd=password, db=database)



def create_tx_log():
    try:
        cur = conn.cursor()
        sql = """CREATE TABLE t_tx( \
                    txid char(64), \
                    vout int, \
                    address char(35), \
                    redeemScript char(44), \
                    scriptPubKey char(46), \
                    amount Decimal(16,8), \
                    confirmations bigint, \
                    spendable char(8),  \
                    solvable char(8), \
                    safe char(8), \
                    blockhash char(64),\
                    created timestamp, \
                    primary key(address))"""
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()
        print(traceback.format_exc())

if __name__ == '__main__':
    create_tx_log()

	
	


