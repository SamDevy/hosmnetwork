import aiohttp
import asyncio
import logging
from utils.telegram import TelegramBot
from utils.transaction_type import get_transaction_type
from utils.exchange_addresses import EXCHANGE_ADDRESSES 


class EthereumTracker:
    def __init__(self, bot_token, chat_id, alchemy_url):
        self.bot = TelegramBot(bot_token, chat_id)
        self.alchemy_url = alchemy_url
        self.last_block = None
        logging.basicConfig(level=logging.INFO)
        
    async def get_latest_block(self):
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_blockNumber",
            "params": [],
            "id": 1
        }    
        async with aiohttp.ClientSession() as session:
            async with session.post(self.alchemy_url, json=payload) as resp:
                data = await resp.json()
                # Return the latest block number, not transaction
                return int(data["result"], 16)
            
    async def get_block_transactions(self, block_number):
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_getBlockByNumber",
            "params": [hex(block_number), True],
            "id": 1
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.alchemy_url, json=payload) as resp:
                data = await resp.json()
                return data["result"]["transactions"]
        
    async def run(self):
        logging.info("ETH TRACKER IS RUNNING")
        
        while True:
            try:
                latest_block = await self.get_latest_block()
                    
                if latest_block != self.last_block:
                    logging.info(f"New block ETH: {latest_block}") 
                    self.last_block = latest_block
                    
                    transactions = await self.get_block_transactions(latest_block)
                    
                    for tx in transactions:
                        eth_value = int(tx["value"], 16) / 1e18
                        
                        if eth_value >= 6000:
                            tx_type = get_transaction_type(tx["from"], tx["to"])
                            message = (
                                f"🚨 Ethereum 🚨\n"
                                f"Transaction Type: {tx_type}\n"
                                f"🐳Value🐳: {eth_value:.2f} ETH\n"
                                f"From: {tx['from']}\n"
                                f"To: {tx['to']}\n"
                                f"https://etherscan.io/tx/{tx['hash']}"
                            )

                            await self.bot.send_message(message)
                
                await asyncio.sleep(5)  

            except Exception as e:
                logging.error(f"Error in Ethereum tracker: {e}")
                await asyncio.sleep(5)  
