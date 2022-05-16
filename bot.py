import datetime
from enum import IntEnum
from typing import Literal
from khl import Bot, Message, Event, EventTypes
from khl.card import Card, CardMessage, Module, Element, Types

from config.config import Config

bot = Bot('1/MTA5NjE=/nekFi+hRk9Pqm+4BQuzAwA==')


class Action:

    def __init__(self, type: Literal['b', 'p'], content: str,
                 user_id: str | int):
        self.type = type
        self.time = datetime.datetime.now()
        self.content = content
        self.user_id = user_id


class MatchTypes(IntEnum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    IS_OVER = 2


class Match:

    _player_1_id: str | int
    _player_1_channel_id: str | int
    _player_1_acntion_reocrd: list[Action] = list()

    _player_2_id: str | int
    _player_2_channel_id: str | int
    _player_2_acntion_reocrd: list[Action] = list()

    _create_time: datetime.datetime
    _match_type: MatchTypes = MatchTypes.NOT_STARTED

    def __init__(self, player_1_id: str | int, player_1_channel_id: str | int,
                 player_2_id: str | int, player_2_channel_id: str | int):
        self._player_1_id = player_1_id
        self._player_1_channel_id = player_1_channel_id
        self._player_2_id = player_2_id
        self._player_2_channel_id = player_2_channel_id

    async def create_match(self):
        self._match_type = MatchTypes.IN_PROGRESS
        await bot.send_message(self._player_1_channel_id, 'Match created!')
        await bot.send_message(self._player_2_channel_id, 'Match created!')

    async def end_match(self):
        self._match_type = MatchTypes.IS_OVER
        await bot.send_message(self._player_1_channel_id, 'Match ended!')
        await bot.send_message(self._player_2_channel_id, 'Match ended!')


config = Config()
is_super_user_message = lambda msg: msg.author_id in config.SUPER_USER_IDS
is_super_user_event = lambda e: e.body['user_id'] in config.SUPER_USER_IDS


@bot.command(regex=r'创建比赛', rules=[is_super_user_message])
async def create_match(msg: Message, bot: Bot):
    await msg.reply(
        CardMessage(
            Card(Module.Section('比赛创建', Element.Button('创建比赛', 'test')))))


@bot.on_event(EventTypes.MESSAGE_BTN_CLICK)
async def click_btn(bot: Bot, event: Event):
    ...


bot.run()