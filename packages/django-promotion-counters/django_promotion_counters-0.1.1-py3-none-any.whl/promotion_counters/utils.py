from typing import Callable

from promotion_counters.action import reward_registry


def on_achievement_callback(verbose_name: str = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        func.verbose_name = verbose_name or func.__name__
        reward_registry.register_callback(func)
        return func

    return decorator
