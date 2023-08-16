from src.sync_env.sync_env import SyncEnv, GenerateEnv


class EnvA(SyncEnv):
    one = None
    two = None


class EnvB(SyncEnv):
    two = None
    three = None


ge = GenerateEnv([
    EnvA,
    EnvB
])

ge.generate()
