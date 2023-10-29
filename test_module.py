from web3 import Web3
from time import sleep


class Balancer:
    def __init__(self, rpc_list):
        print("balancer initiated")
        self.__balancer = {}
        self.rpc_list = rpc_list
        for network in self.rpc_list:
            self.__balancer[network] = 0

    def w3(self, network):
        self.__balancer[network] += 1
        self.__balancer[network] = self.__balancer[network] % len(
            self.rpc_list[network]['links'])
        rpc_url = self.rpc_list[network]['links'][self.__balancer[network]]
        w3 = Web3(Web3.HTTPProvider(
            self.rpc_list[network]['links'][self.__balancer[network]]))
        return w3

    def execute_web3_function(self, network, function_name, *args, **kwargs):
        w3 = self.w3(network)
        func = getattr(w3, function_name)
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error executing web3 function: {str(e)}")
            return None

    def __getattr__(self, attr):
        if attr.startswith('__') and attr.endswith('__'):
            # Handle double underscore methods
            return super().__getattr__(attr)
        else:
            # Handle regular function calls
            return self._handle_function_call(attr)

    def _handle_function_call(self, attr):
        def inner(*args, **kwargs):
            function_str = attr
            if args:
                function_str += '.' + '.'.join(args)
            print(function_str)

        return inner
