# utils/transaction_type.py

from utils.exchange_addresses import EXCHANGE_ADDRESSES

def get_transaction_type(from_address: str, to_address: str) -> str:
    """
    This function checks the sender and receiver addresses
    to determine whether the transaction is a Buy, Sell, or Transfer.

    - Buy: from exchange → to unknown wallet
    - Sell: from unknown wallet → to exchange
    - Transfer: anything else
    """

    from_addr = from_address.lower()
    to_addr = to_address.lower()

    # Flatten all exchange addresses into one list
    all_exchange_addresses = [addr.lower() for addresses in EXCHANGE_ADDRESSES.values() for addr in addresses]

    # Check patterns
    if from_addr in all_exchange_addresses and to_addr not in all_exchange_addresses:
        return "Buy"
    elif to_addr in all_exchange_addresses and from_addr not in all_exchange_addresses:
        return "Sell"
    else:
        return "Transfer"
