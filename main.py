import os
import asyncio
from dotenv import load_dotenv

from trackers.ethereum_tracker import EthereumTracker
from trackers.bitcoin_tracker import BitcoinTracker
from trackers.solana_tracker import SolanaTracker

# تحميل المتغيرات
load_dotenv()

print("ETH_BOT_TOKEN:", os.getenv("ETH_BOT_TOKEN"))
print("TELEGRAM_CHAT_ID:", os.getenv("TELEGRAM_CHAT_ID"))
print("ALCHEMY_API_URL:", os.getenv("ALCHEMY_API_URL"))


# قراءة من .env
eth_token = os.getenv("ETH_BOT_TOKEN")
btc_token = os.getenv("BTC_BOT_TOKEN")
sol_token = os.getenv("SOL_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
alchemy_url = os.getenv("ALCHEMY_API_URL")

print("ETH type:", type(eth_token))
print("Chat ID type:", type(chat_id))
print("Alchemy URL type:", type(alchemy_url))

# تمرير القيم بشكل صحيح
eth_tracker = EthereumTracker(str(eth_token), str(chat_id), str(alchemy_url))
btc_tracker = BitcoinTracker(str(btc_token), str(chat_id))
sol_tracker = SolanaTracker(str(sol_token), str(chat_id))

async def main():
    await asyncio.gather(
        eth_tracker.run(),
        btc_tracker.run(),
        sol_tracker.run()
    )

print("running all bots")
asyncio.run(main())
