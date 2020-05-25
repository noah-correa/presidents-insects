from player import Player

class Bot(Player):

    __idBot = 0

    @classmethod
    def generate_idBot(cls):
        Bot.__idBot += 1
        return Bot.__id

    def __init__(self):
        self.__idBot = Bot.generate_idBot()
        super().__init__(f"Bot {self.__idBot}")