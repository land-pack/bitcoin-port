Install Bitcore 
===


* 1. Install NVM

	> 		curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
	>		source ~/.bashrc
	>		nvm install v4

* 2.Install ZeroMQ

	> 		sudo dnf install zeromq.x86_64
	>		sudo dnf install cppzeromq-devel.x86_64
	
	
* 3.Install RocksDB

	>		sudo dnf install rocksdb-devel.x86_64
	>		sudo dnf install rocksdb.x86_64

* 4.Install RocksDB Python API

	>		sudo dnf install lzip.x86_64
	>		sudo dnf install snappy.x86_64
	>		sudo dnf install python-snappy.x86_64
	
	>		sudo dnf install python3-devel.x86_64
	>		pip install virtualenv
	>		virtualenv -p /usr/bin/python3 ~/venv/py3
	
* 5.Install bitcoin

	>		npm install -g bitcore


* 6.Install Bitcoind
	
	>Download it from the offical website, and put its path to the `bitcore-node.json` configration.
	
		https://bitcoin.org/bin/bitcoin-core-0.16.2/bitcoin-0.16.2-x86_64-linux-gnu.tar.gz

* 7.Configuration

		{
		  "network": "livenet",
		  "port": 3001,
		  "services": [
		    "bitcoind",
		    "web",
		    "insight-api-dash",
		    "insight-ui-dash"
		  ],
		  "servicesConfig": {
		    "bitcoind": {
		      "spawn": {
		        "datadir": "/home/dev/.bitcore/data",
		        "exec": "/home/dev/.bitcore/data/dashd"
		      }
		    }
		  }
		}
