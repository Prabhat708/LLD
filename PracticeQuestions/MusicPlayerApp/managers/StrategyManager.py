from enums.PlayStrategyType import PlayStrategyType
from strategies.SequentialPlayStrategy import SequentialPlayStrategy
from strategies.RandomPlayStrategy import RandomPlayStrategy
from strategies.CustomQueueStrategy import CustomQueueStrategy


class StrategyManager:
    _instance = None

    def __init__(self):
        self.sequential_strategy = SequentialPlayStrategy()
        self.random_strategy = RandomPlayStrategy()
        self.custom_queue_strategy = CustomQueueStrategy()

    @staticmethod
    def get_instance():
        if StrategyManager._instance is None:
            StrategyManager._instance = StrategyManager()
        return StrategyManager._instance

    def get_strategy(self, strategy_type):
        if strategy_type == PlayStrategyType.SEQUENTIAL:
            return self.sequential_strategy
        elif strategy_type == PlayStrategyType.RANDOM:
            return self.random_strategy
        else:
            return self.custom_queue_strategy
