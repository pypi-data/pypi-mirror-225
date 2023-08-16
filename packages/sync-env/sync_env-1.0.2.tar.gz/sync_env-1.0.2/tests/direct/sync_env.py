import os

from src.sync_env.sync_env import SyncEnv

os.environ["NONE"] = "のん"


class Env(SyncEnv):

    TEST = "test"
    VALUE = None
    NONE: str = None
    NEW_ENV = None


env = Env()


if __name__ == "__main__":
    print(env.TEST)
    print(env.VALUE)
    print(env.NONE)
