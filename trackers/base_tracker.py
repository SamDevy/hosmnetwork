from abc import ABC, abstractmethod

class BaseTracker(ABC):
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id

    @abstractmethod
    async def run(self):
        """
        Method that must be implemented by all subclasses.
        Should contain the main loop logic for checking transactions.
        """
        pass
