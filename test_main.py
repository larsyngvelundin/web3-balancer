# from main import Balancer
# from web3 import Web3
from test_module import Balancer
from rpc_list import rpc_list
w3 = Balancer(rpc_list)
print(w3.test.tester())
print(w3.is_connected())
print(w3.eth.block_number)

# Calls the dynamic_function with name = "search" and arguments ("test",)
# module.search("test")


swap_list = {}
net = "eth"
swap_list[net] = {}
swap = "swap_test"
swap_list[net][swap] = "test"
abi = {}
abi["swaps"] = {}
abi["swaps"][net] = {}
abi["swaps"][net][swap] = "abi_test"


# module.eth.contract(address=Web3.to_checksum_address(
#     swap_list[net][swap]['address']), abi=abi.swaps[net][swap])
