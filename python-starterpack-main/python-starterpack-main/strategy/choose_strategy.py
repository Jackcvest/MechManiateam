from strategy.random_strategy import RandomStrategy
from strategy.simple_human_strategy import SimpleHumanStrategy
from strategy.simple_zombie_strategy import SimpleZombieStrategy
from strategy.Jericho_strategy import TestSetupStrategy
from strategy.strategy import Strategy
<<<<<<< HEAD
from strategy.Jericho_strategy import TestSetupStrategy

=======
from strategy.VestZombie import VestZombieStrategy
>>>>>>> 1b474f26622d15877968c37608645ae1cf5b1519

def choose_strategy(is_zombie: bool) -> Strategy:
    # Modify what is returned here to select the strategy your bot will use
    # NOTE: You can use "is_zombie" to use two different strategies for humans and zombies (RECOMMENDED!)
    #
<<<<<<< HEAD

    if is_zombie:
        return SimpleZombieStrategy()
    else:
        return TestSetupStrategy()

=======
    # For example:
    if is_zombie:
        return VestZombieStrategy()
    else:
        return TestSetupStrategy()
>>>>>>> 1b474f26622d15877968c37608645ae1cf5b1519
