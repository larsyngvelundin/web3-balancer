from time import sleep
import requests

from web3 import Web3
from web3.middleware import geth_poa_middleware
from loguru import logger


class Balancer:
    def __init__(self, rpc_list, tor=False, name=""):
        logger.debug('init started')
        self.balancer = {}
        self.tor = tor
        self.rpc_list = rpc_list
        for network in self.rpc_list:
            self.balancer[network] = 0
        self._name = name

    def __getattr__(self, name):
        # Create a new instance with the updated name
        return Balancer(f"{self._name}.{name}")

    def __call__(self, *args, **kwargs):
        try:
            # Perform the desired functionality with the arguments
            print(
                f"Calling function {self._name} with arguments: {args}, {kwargs}")
        except Exception as e:
            # Handle any errors
            print(f"An error occurred: {str(e)}")


# class Balancer():
#     def __init__(self, rpc_list, tor=False):
#         logger.debug('init started')
#         self.balancer = {}
#         self.tor = tor
#         self.rpc_list = rpc_list
#         for network in self.rpc_list:
#             self.balancer[network] = 0

#     def w3(self, network):
#         self.balancer[network] += 1
#         self.balancer[network] = self.balancer[network] % len(
#             self.rpc_list[network]['links'])
#         if (self.tor):
#             session = get_tor_session()
#             w3 = Web3(Web3.HTTPProvider(
#                 self.rpc_list[network]['links'][self.balancer[network]], session=session))
#         if (network == "matic" or network == "bnb"):
#             w3.middleware_onion.inject(geth_poa_middleware, layer=0)
#         if (w3.is_connected()):
#             logger.debug(
#                 f"Returning W3 on {self.rpc_list[network]['links'][self.balancer[network]]}")
#             return w3
#         else:
#             logger.debug(
#                 f"Unable to connect to {self.rpc_list[network]['links'][self.balancer[network]]}")
#             sleep(0.5)
#             return self.w3(network)


# balancer.run(function)
# do the function call thing from the scanner
# return error if function is not found


url = "http://ip-api.com/json/"


def get_tor_session():
    session = requests.Session()
    session.proxies = {
        'http': 'socks5h://localhost:9050',
        'https': 'socks5h://localhost:9050',
    }

    adapter = requests.adapters.HTTPAdapter(
        pool_connections=20, pool_maxsize=20)

    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response = session.get(url)
    logger.debug(response.text)

    return session
