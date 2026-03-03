from web3 import Web3
import os

# ================= RPC LIST (Fallback) =================

RPC_LIST = [
    os.getenv("RPC_MAINNET", "https://eth.llamarpc.com"),
    "https://rpc.ankr.com/eth",
    "https://cloudflare-eth.com"
]


def get_web3():
    """
    Try RPC list one by one until connected
    """
    for rpc in RPC_LIST:
        try:
            w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={'timeout': 5}))
            if w3.is_connected():
                return w3
        except:
            continue
    return None


# ================= VALIDATE ADDRESS =================

def is_valid_address(address):
    try:
        return Web3.is_address(address)
    except:
        return False


# ================= GET EVM BALANCE =================

def get_balance(address):
    """
    Return balance in ETH (float)
    """

    if not address:
        return 0

    if not is_valid_address(address):
        return 0

    w3 = get_web3()

    if not w3:
        return 0

    try:
        checksum = Web3.to_checksum_address(address)
        balance_wei = w3.eth.get_balance(checksum)
        balance_eth = w3.from_wei(balance_wei, "ether")
        return round(float(balance_eth), 6)
    except:
        return 0


# ================= GET TOKEN BALANCE (ERC20) =================

def get_token_balance(address, token_contract):
    """
    Get ERC20 token balance
    """

    if not is_valid_address(address) or not is_valid_address(token_contract):
        return 0

    w3 = get_web3()
    if not w3:
        return 0

    try:
        abi = [{
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function"
        }]

        contract = w3.eth.contract(
            address=Web3.to_checksum_address(token_contract),
            abi=abi
        )

        balance = contract.functions.balanceOf(
            Web3.to_checksum_address(address)
        ).call()

        return balance

    except:
        return 0


# ================= MULTI WALLET SCAN =================

def scan_multiple(wallets):
    """
    Scan multiple wallets (list)
    Return dict {address: balance}
    """
    result = {}

    for w in wallets:
        result[w] = get_balance(w)

    return result