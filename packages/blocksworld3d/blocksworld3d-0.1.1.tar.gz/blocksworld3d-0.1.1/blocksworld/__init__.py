import gymnasium as gym
from .blocksworld import BlocksWorld

__all__ = ["BlocksWorld"]

gym.register(
    id="BlocksWorld-v0",
    entry_point="blocksworld:BlocksWorld",
)
