
class GameConfig:
    _instance = None

    def __init__(self):
        GameConfig._instance = self
        self.difficulty = 1
        self.max_turns = 5

    @staticmethod
    def getInstance():
        if GameConfig._instance is None:
            GameConfig()
        return GameConfig._instance
