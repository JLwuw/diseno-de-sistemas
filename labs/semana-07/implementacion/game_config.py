from __future__ import annotations


class GameConfig:
    _instance = None

    def __init__(self):
        self.difficulty = 1
        self.max_turns = 5

    @staticmethod
    def get_instance() -> GameConfig:
        if GameConfig._instance is None:
            GameConfig._instance = GameConfig()

        return GameConfig._instance
