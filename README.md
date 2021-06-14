localcrypto is a naive cryptocurrency, created for the intellectual exercise.

It is a work in progress. Currently, it only provides the tools for running a node and sending transactions with a wallet. It does not include a finalized script for actually doing those things. 

## Requirements
This program requires Python 3.7.6. 
I have only tested with Python 3.7.6, though it should work with Python>=3.7.6

To install all necessary Python packages, run

    pip install -r requirements.txt

while in the localcrypto directory.

## Running an example
First, while in the outermost localcrypto directory, run the following command:

    python setup.py develop

This will make localcrypto a package on your machine so you can import it.

Second, open two terminal windows. In both, navigate to localcrypto/localcrypto.

Finally, run the following command in one window:

    python run_mining_node.py

And run the following command in the other window:

    python send_tx_to_node.py

To stop the node, kill the process with CTRL+C.

