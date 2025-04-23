import aiohttp
import asyncio
import logging
from utils.telegram_sender import send_telegram_message

class SolanaTracker:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = "https://api.helius.xyz/v0/addresses"
        self.wallet_addresses = [
            "9rfog2YXgX78tVghAytBXJhuLdo95dtSkJdT3U3Zxe3q",
            "H3sGbLqVXpoX9G8zFnQmDD7pX3VgNm7u9f14hswFikYs",
            "5JdiLby8EuWoK5tGoYJmuV3GkSseHvL1ftKvqLPub7kV",
        ]
        self.api_key = "a55f0597-c928-4272-a0f6-83469717947e"

    async def fetch_latest_transactions(self, wallet_address):
        url = f"{self.api_url}/{wallet_address}/transactions?api-key={self.api_key}&limit=1"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                logging.warning(f"⚠️ فشل في جلب المعاملات من {wallet_address}: {response.status}")
                return []

    def get_transaction_type(self, tx):
        try:
            if "events" in tx:
                events = tx["events"]
                if events.get("nft"):
                    return "NFT Trade"
                if events.get("swap"):
                    return "Swap (Buy/Sell)"
                if events.get("stake"):
                    return "Stake"
            for instr in tx.get("instructions", []):
                program = instr.get("program", "").lower()
                if program == "system":
                    return "Transfer"
                if "raydium" in program or "jupiter" in program:
                    return "Buy/Sell"
            return "Unknown"
        except Exception as e:
            return f"Error: {e}"

    async def check_large_transactions(self):
        for wallet in self.wallet_addresses:
            transactions = await self.fetch_latest_transactions(wallet)
            for tx in transactions:
                sol = tx.get("amount", 0) / 1_000_000_000
                usd_amount = sol * 150  # تقدير تقريبي

                if usd_amount >= 100:
                    tx_type = self.get_transaction_type(tx)
                    message = (
                        f"🚨 SOLANA 🚨\n"
                        f"Transaction over $100K!\n"
                        f"Type: {tx_type}\n"
                        f"🐳Amount🐳: ${usd_amount:,.2f}\n"
                        f"Wallet: {wallet}\n"
                        f"Signature: {tx.get('signature')}"
                    )
                    await send_telegram_message(self.bot_token, self.chat_id, message)

    async def run(self):
        logging.getLogger("trackers.solana_tracker").setLevel(logging.INFO)
        while True:
            try:
                await self.check_large_transactions()
            except Exception as e:
                logging.error(f"Solana tracker error: {e}")
            await asyncio.sleep(10)
