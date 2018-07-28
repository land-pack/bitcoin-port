# How to sync chain's data to your local database

You have to run your node with following mode:

    ./bitcoind -rpcbind=0.0.0.0:8332 -server -rest=1 -zmqpubhashtx=tcp://0.0.0.0:28332 -txindex=1 -reindex
 

Create the table by run:

    python create_table.py
