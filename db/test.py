import mysql.connector

cnx = mysql.connector.connect(user='frank', password='openmysql', 
                                host='192.168.1.86',
                                database='test')

cnx.close()

"""
It is also possible to create connection objects using the connection.MySQLConection() class:
"""

from mysql.connector import (connection)

cnx = connection.MySQLConnection(user='frank', password='openmysql',
                                host='192.168.1.86',
                                database='test')

cnx.close()
