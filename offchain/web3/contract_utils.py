from eth_utils import function_signature_to_4byte_selector  # type: ignore[attr-defined]


def function_signature_to_sighash(signature: str) -> str:
    """Takes an human-readable function signature (ex: 'supportsInterface(bytes4)') and returns the
    signature hash that would be present in the evm bytecode.

    Args:
        signature (str): human readable function signature

    Returns:
        str: hash present in evm bytecode
    """  # noqa: E501
    return "0x" + function_signature_to_4byte_selector(signature).hex()
