import asyncio
from dataclasses import dataclass
from functools import cached_property
from typing import Any, Literal, Optional, Union

import aiohttp
from eth_abi import decode_abi, encode_abi
from eth_utils import to_hex
from web3 import Web3
from web3.eth import AsyncEth

from offchain.web3.contract_utils import function_signature_to_sighash


def make_async_w3_client(url: str, request_kwargs: dict = {"timeout": 20}) -> Web3:
    """Return default EVM compatible web3py client"""
    w3 = Web3(
        Web3.AsyncHTTPProvider(url, request_kwargs=request_kwargs),  # type: ignore[arg-type]
        modules={"eth": (AsyncEth,)},
        middlewares=[],
    )
    return w3


@dataclass
class AsyncContractReader:
    rpc_url: str

    @cached_property
    def async_w3(self) -> Web3:
        """Async web3py client instance configured for a specific chain (EVM chain)"""
        return make_async_w3_client(self.rpc_url)

    async def call_function(
        self,
        contract_address: str,
        function_signature: str,
        return_type: list[str],
        args: Optional[list[Any]] = None,
    ) -> Optional[Any]:
        result = await self._request(
            method="eth_call",
            params=[
                {
                    "to": contract_address,
                    "data": self._encode_params(function_signature, args),
                }
            ],
        )

        return self._decode_result(
            result, return_type
        )  # type:ignore[return-value,arg-type]

    async def gen_call_single_function_single_address_many_args(
        self,
        address: str,
        function_sig: str,
        return_type: list[str],
        args: list[list[Any]],
        block_tag: Optional[str] = "latest",
        **kwargs,
    ) -> list[Optional[Any]]:
        """Call a single function on a single address with many different permutations of arguments

        Args:
            address (str): address to call function on
            function_sig (str): function signature (ex: "totalSupply()")
            return_type (list[str]): return function signature (ex: ["uint256"])
            args (list[list[Any]]): list of arguments passed in each fn call (ex: [[1], [2], [3]])
            chunk_size (int, optional): chunk size. Defaults to 500.

        Returns:
            list[Optional[Any]]: list of returned values, mapped 1-1 with args
        """

        req_params = [
            self.view_request_builder(address, function_sig, arg, block_tag, **kwargs)
            for arg in args
        ]

        res = await self.gen_multi_call("eth_call", req_params, block_tag)
        return list(map(lambda x: self._decode_result(x, return_type), res))

    async def gen_call_single_function_many_address_ordered_args(
        self,
        addresses: list[str],
        function_signature: str,
        return_type: list[str],
        args: list[list[Any]],
        block_tag: Optional[str] = "latest",
    ) -> list[Any]:
        """Call a function with many addresses with no arguments asychronously

        Args:
            addresses (list[str]): list of addresses
            function_signature (str): function signature (e.g. "balanceOf(address)")
            return_type (list[str]): single return type (e.g. ["uint256"])
            block_tag (Optional[str], optional): block tag. Defaults to "latest".
            chunk_size (int, optional): chunk size. Defaults to 500.

        Returns:
            [list[any]]: mapped 1-1 with addresses, all of same type
        """

        req_params = [
            self.view_request_builder(
                addresses[i], function_signature, args[i], block_tag
            )
            for i in range(len(addresses))
        ]

        res = await self.gen_multi_call("eth_call", req_params, block_tag)
        return list(map(lambda x: self._decode_result(x, return_type), res))

    async def gen_call_ordered_function_many_address_ordered_args(
        self,
        addresses: list[str],
        function_sigs: list[str],
        return_types: list[list[str]],
        args: list[list[Any]],
        block_tag: Optional[str] = "latest",
    ) -> list[Any]:
        """Call an ordered set of functions with args on an ordered set of addresses

        Args:
            addresses (list[str]): list of addresses
            function_sigs (list[str]): list of function signatures (ex: ["totalSupply()"])
            return_types (list[list[str]]): list of return function signature (ex: [["uint256"]])
            args (list[list[Any]]): list of arguments passed in each fn call (ex: [[1], [2], [3]])

        Returns:
            [list[Any]]: mapped 1-1 with addresses, may be of varying types
        """

        req_params = [
            self.view_request_builder(
                addresses[i], function_sigs[i], args[i], block_tag
            )
            for i in range(len(addresses))
        ]

        res = await self.gen_multi_call("eth_call", req_params, block_tag)
        return list(
            map(lambda x: self._decode_result(res[x], return_types[x]), range(len(res)))
        )

    async def gen_multi_call(
        self,
        method: str,
        params: list[list[Any]],
        block_tag: Optional[str] = "latest",
    ) -> list[Any]:
        result = await asyncio.gather(
            *[
                self._request(method, param, block_tag)  # type:ignore[arg-type]
                for param in params
            ]
        )
        return result

    def view_request_builder(
        self,
        address: str,
        function_sig: str,
        args: Optional[list] = None,
        block_tag: Optional[str] = "latest",
        **kwargs,
    ):
        """Request generation function. Can be overloaded via inheritance for custom RPC requests.

        Args:
            address (str): address to call
            function_sig (str): function signature
            args (Optional[list], optional): arguments for function if present

        Returns:
            [type]: [description]
        """
        data = self._encode_params(function_sig, args, **kwargs)
        return [{"to": address, "data": data}, block_tag]

    async def get_owner(self, contract_address: str) -> Optional[str]:
        """Read the owner() function of a contract"""
        return await self.call_function(  # type:ignore[return-value]
            contract_address, "owner()", return_type=["address"]
        )

    async def get_code(self, contract_address: str) -> Optional[Any]:
        """getCode() for a specific address"""
        return await self._request(  # type:ignore[return-value]
            method="eth_getCode",
            params=[contract_address],
        )

    async def _request(
        self,
        method: str,
        params: Optional[list[Any]] = None,
        block_tag: Optional[Union[Literal["latest"], int]] = None,
    ) -> Optional[Union[Any, tuple[Any]]]:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
        }

        if params:
            if block_tag is None:
                params.append("latest")
            payload["params"] = params

        # Make an async call with aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(self.rpc_url, json=payload) as response:
                response_json = await response.json()
            return response_json.get("result")

    @staticmethod
    def _encode_params(
        function_sig: str,
        args: Optional[list] = None,
        arg_types: Optional[list] = None,
        **kwargs,
    ) -> str:
        """Encode eth_call data by first taking the function sighash, then adding the encoded data

        Args:
            function_sig (str): function signature
            args (Optional[list], optional): arguments to pass. Defaults to None.

        Returns:
            str: [description]
        """
        b = bytes.fromhex(function_signature_to_sighash(function_sig)[2:])
        if args is not None:
            if arg_types is None:
                start = function_sig.find("(")
                arg_types = function_sig[start:].strip("()").split(",")
                if type(arg_types) is str:
                    arg_types = [arg_types]
            b += encode_abi(arg_types, args)
        p = to_hex(b)
        return p

    @staticmethod
    def _decode_result(
        result: Optional[Any], return_types: list[str]
    ) -> Optional[Union[Any, tuple[Any]]]:
        """Decode responses, filling None for any errored requests

        Args:
            result (str): [description]
            return_types (list[str]): [description]

        Returns:
            Optional[Union[Any, tuple[Any]]]: none if error, single value or multiple values
                depending on what the contract call returns
        """
        try:
            if result is None:
                return None
            trimmed = result[2:]
            if trimmed == "":
                return None
            parsed = decode_abi(return_types, bytes.fromhex(trimmed))
            n_expected, n_received = len(return_types), len(parsed)
            if n_expected == 1 or n_received == 1:
                return parsed[0]
            elif n_expected < n_received:
                return parsed[:n_expected]
            else:
                return parsed
        except Exception:
            return None
