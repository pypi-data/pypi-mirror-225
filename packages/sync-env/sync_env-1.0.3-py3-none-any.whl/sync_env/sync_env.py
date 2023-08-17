import os


class SyncEnv:

    def __init__(self) -> None:

        not_exist_env_list = []

        for key in dir(self):
            if key[0] == "_":
                continue
            value = getattr(self, key)
            env_value = os.getenv(key)
            if env_value is None:
                not_exist_env_list.append(key)
            setattr(self, key, env_value if env_value else value)
        # self.__generate_env(not_exist_env_list)

    # def __generate_env(self, not_exist_env_list: list[str]):

    #     if not not_exist_env_list:
    #         return

    #     print("generate env")

    #     with open(".env", "r", encoding="utf-8") as f:
    #         texts = f.read().split("\n")

    #     with open(".env", "a", encoding="utf-8") as f:
    #         for key in not_exist_env_list:
    #             add = f"{key}="
    #             if add in texts:
    #                 continue
    #             print(f"added {key}")
    #             f.write(f"{add}\n")


class GenerateEnv:

    class_list: list[type(SyncEnv)]

    def __init__(self, class_list: list[type(SyncEnv)]) -> None:
        self.class_list = class_list

    def generate(self, path=".env"):
        value_list = []
        for c in self.class_list:
            o = c()
            for key in dir(o):
                if key[0] == "_":
                    continue
                if key in value_list:
                    continue
                value_list.append(key)
        last_enter = False
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
            if text[-1] != "\n":
                last_enter = True
            envs = [l.split("=")[0] for l in text.split("\n")]

        with open(path, "a", encoding="utf-8") as f:
            if last_enter:
                f.write("\n")
            for value in value_list:
                if value in envs:
                    continue
                f.write(f"{value}=\n")
