import aiohttp
import asyncio
import logging
from utils.telegram import TelegramBot
from utils.transaction_type import get_transaction_type
from utils.exchange_addresses import EXCHANGE_ADDRESSES

logger = logging.getLogger(__name__)

class BitcoinTracker:
    def __init__(self, bot_token, chat_id):
        self.bot = TelegramBot(bot_token, chat_id)
        self.last_tx_ids = set()  # لتجنب تكرار المعاملات
        logging.basicConfig(level=logging.INFO)

    async def fetch_latest_transactions(self):
        url = "https://blockstream.info/api/mempool/recent"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise Exception("فشل في جلب معاملات البيتكوين")
                return await resp.json()

    async def get_transaction_details(self, txid):
        url = f"https://blockstream.info/api/tx/{txid}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise Exception("فشل في جلب تفاصيل المعاملة")
                return await resp.json()

    async def run(self):
        logging.info("BitcoinTracker Started")

        while True:
            try:
                latest_txs = await self.fetch_latest_transactions()
                for tx in latest_txs:
                    txid = tx.get("txid")

                    if txid in self.last_tx_ids:
                        continue

                    self.last_tx_ids.add(txid)

                    tx_details = await self.get_transaction_details(txid)

                    # حساب القيمة الإجمالية الداخلة (input) والخارجة (output)
                    total_input = sum(i.get('prevout', {}).get('value', 0) for i in tx_details.get('vin', [])) / 1e8
                    total_output = sum(o.get('value', 0) for o in tx_details.get('vout', [])) / 1e8

                    btc_value = max(total_input, total_output)  # ناخذ الأعلى كقيمة حقيقية تقريبًا

                    if btc_value >= 500:  # المعاملات الكبيرة فقط
                        from_address = tx_details.get('vin', [{}])[0].get('prevout', {}).get('scriptpubkey_address', 'N/A')
                        to_address = tx_details.get('vout', [{}])[-1].get('scriptpubkey_address', 'N/A')

                        tx_type = get_transaction_type(from_address, to_address)


                        message = (
                            f"🚨 Bitcoin 🚨\n"
                            f"Transaction Type: {tx_type}\n"
                            f"🐳Value🐳: {btc_value:.2f} BTC🐳\n"
                            f"From: {from_address}\n"
                            f"To: {to_address}\n"
                            f"https://mempool.space/tx/{txid}"
                        )

                        await self.bot.send_message(message)

                await asyncio.sleep(5)

            except Exception as e:
                logging.error(f"خطأ في Bitcoin tracker: {e}")
                await asyncio.sleep(5)
