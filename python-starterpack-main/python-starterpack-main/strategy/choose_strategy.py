from strategy.random_strategy import RandomStrategy
from strategy.simple_human_strategy import SimpleHumanStrategy
from strategy.simple_zombie_strategy import SimpleZombieStrategy
from strategy.strategy import Strategy


def choose_strategy(is_zombie: bool) -> Strategy:
    # Modify what is returned here to select the strategy your bot will use
    # NOTE: You can use "is_zombie" to use two different strategies for humans and zombies (RECOMMENDED!)
    #
    # For example:
    # if is_zombie:
    #     return SimpleZombieStrategy()
    # else:
    #     return SimpleHumanStrategy()

    return RandomStrategy()
