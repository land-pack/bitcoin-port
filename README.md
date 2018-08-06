# bitcoin-port
API For Bitcoin Write By Flask



# ./bitcoind -testnet -rpcbind=0.0.0.0:8332 -server -rest=1



# The Best Solution.

    docker pull sena/bitcore
    docker run -d --restart=always --name bitcore_server -p 3001:3001 -p 8338:8333 -v /data/.bitcore:/root/.bitcore sena/bitcore
