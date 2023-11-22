from time import sleep
import requests

from web3 import Web3
from web3.providers.rpc import HTTPProvider
import web3
from web3.middleware import geth_poa_middleware
from loguru import logger


class Web3_balancer():
    def __init__(self, rpc_list, tor=False, is_contract=False, w3=None, set_net=""):
        self.error_count = 0
        self.curr_func = ""
        self.is_contract = is_contract
        self.net = set_net
        self._active_net = set_net
        self.rpc_list = rpc_list
        self.balancer = {}
        for network in self.rpc_list:
            self.balancer[network] = 0
        self.tor = tor
        self._w3 = w3

    def get_w3(self, network):
        self._active_net = network
        self.balancer[network] += 1
        self.balancer[network] = self.balancer[network] % len(
            self.rpc_list[network]['links'])

        if (self.tor):
            session = get_tor_session()
            w3 = Web3(Web3.HTTPProvider(
                self.rpc_list[network]['links'][self.balancer[network]], session=session))
        else:
            w3 = Web3(Web3.HTTPProvider(
                self.rpc_list[network]['links'][self.balancer[network]]))
        if (self.is_contract):
            self.is_contract = w3.eth.contract(
                address=self.is_contract.address, abi=self.is_contract.abi)

        if (network == "matic" or network == "bnb"):
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        try:
            if (self.is_contract):
                if (self.is_contract.w3.is_connected()):
                    logger.debug(
                        f"W3 connected to {self.rpc_list[network]['links'][self.balancer[network]]}")
                    self._active_net = network
                    return w3
                else:
                    logger.error(
                        f"Unable to connect to {self.rpc_list[network]['links'][self.balancer[network]]}")
                    sleep(0.5)
                    return self.get_w3(network)

            else:
                if (w3.is_connected()):
                    logger.debug(
                        f"W3 connected to {self.rpc_list[network]['links'][self.balancer[network]]}")
                    self._active_net = network
                else:
                    logger.error(
                        f"Unable to connect to {self.rpc_list[network]['links'][self.balancer[network]]}")
                    logger.debug("Attempting new connection in 0.5s")
                    sleep(0.5)
                    return self.get_w3(network)
        except AssertionError as error:
            logger.error(
                f"Unable to connect to {self.rpc_list[network]['links'][self.balancer[network]]}")
            sleep(0.5)
            return self.get_w3(network)

        return w3

    def __getattr__(self, name):
        self.curr_func += "." + name
        return self

    def __call__(self, *args, **kwargs):
        func_call = self.curr_func[1:]
        if (func_call.find("eth") == 0 and len(args) + len(kwargs) == 0):
            pass
        else:
            arg_str = ', '.join(repr(arg) for arg in args)
            kwarg_str = ""
            for argument in kwargs:
                if argument == "address":
                    kwarg_str += f",{argument} = '{kwargs[argument]}'"
                else:
                    kwarg_str += f",{argument} = {kwargs[argument]}"
            func_call = f"{func_call}({arg_str}{kwarg_str})"
        self.curr_func = ""
        func_call = func_call.replace("(,", "(")
        return self._call_w3_func(func_call)

    def _call_w3_func(self, func):
        if (self._w3 == None or self._active_net != self.net):
            self._w3 = self.get_w3(self.net)
        val = None
        try:
            if (self.is_contract):
                val = eval(f"self.is_contract.{func}")
            else:
                val = eval(f"self._w3.{func}")
        except (requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.HTTPError,
                TimeoutError) as error:
            self.error_count += 1
            if (self.error_count > 1):
                raise Exception(
                    f"Failed to get a working web3 connection {self.error_count} times in a row, aborting.")
            logger.error(error)
            logger.debug(f"Fetching new w3 connection and trying again")
            self._w3 = self.get_w3(self.net)
            if (self.is_contract):
                self.is_contract.w3 = self._w3
            sleep(0.2)
            self._call_w3_func(func)
        if str(type(val)) == "<class 'web3._utils.datatypes.Contract'>":
            logger.debug("Returning a contract balancer")
            contract = Web3_balancer(self.rpc_list, tor=self.tor,
                                     is_contract=val, set_net=self._active_net)
            return contract
        self.error_count = 0
        return (val)


def get_tor_session():
    url = "http://ip-api.com/json/"

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
