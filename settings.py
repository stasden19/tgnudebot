from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int
    token_api: str
    provide_token: str


@dataclass
class Settings:
    bots: Bots


def get_setting(path: str):
    env = Env()
    env.read_env(path)
    return Settings(
        bots=Bots(
            bot_token=env.str('TOKEN'),
            admin_id=env.int('ADMIN_ID'),
            token_api=env.str('TOKEN_API'),
            provide_token=env.str('PROVIDE_TOKEN')
        )
    )


settings = get_setting('input')