import os

from sync_env import SyncEnv
import pytest

os.environ["NONE"] = "のん"


class Env(SyncEnv):

    TEST = "test"
    VALUE = None
    NONE: str = None


env = Env()


def test_():
    assert env.TEST == "test"
    assert env.VALUE == None
    assert env.NONE == "のん"


if __name__ == "__main__":
    print(env.TEST)
    print(env.VALUE)
    print(env.NONE)
