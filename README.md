# web3.py balancer
A class that handles web3 connections and rotates between them to balance out the requests.
## Requirements 
- web3
- tor service running (if you wish to use tor)
- loguru (only for logging)
- List of RPC servers in a dict, see in \examples\rpc_list_formatting.py
## Installation
```
pip install web3_balancer
```
## Usage
```python
>>> from web3_balancer import Web3_balancer
>>> w3 = Web3_balancer(rpc_list)
>>> w3.net = "eth"
```
After setting this up, you can use it as you would normally use web3.

(Except that `block_number` is now `block_number()`)

```python
>>> w3.is_connected()
True
>>> w3.eth.block_number()
18462992
>>> w3.eth.gas_price()
23739122094
```