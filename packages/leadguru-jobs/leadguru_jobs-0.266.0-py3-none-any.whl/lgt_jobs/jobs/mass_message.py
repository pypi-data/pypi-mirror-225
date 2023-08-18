import time
from random import randint
from typing import Optional, Any
from lgt.common.python.slack_client.web_client import SlackWebClient
from lgt_data.mongo_repository import DedicatedBotRepository
from loguru import logger as log
from ..basejobs import BaseBackgroundJobData, BaseBackgroundJob

"""
Send Slack Code
"""


class SendMassMessageSlackChannelJobData(BaseBackgroundJobData):
    text: str
    channel_ids: list[str]
    user_id: str
    files: Optional[list[Any]]
    source_id: str


class SendMassMessageSlackChannelJob(BaseBackgroundJob):
    @property
    def job_data_type(self) -> type:
        return SendMassMessageSlackChannelJobData

    def exec(self, data: SendMassMessageSlackChannelJobData):
        bot = DedicatedBotRepository().get_by_user_and_source_id(data.user_id, data.source_id)
        if not bot or bot.invalid_creds:
            log.warning(f"Bot not found or not invalid creds, source id:{data.source_id}")
            return

        slack_client = SlackWebClient(bot.token, bot.cookies)
        attempts = 0

        for channel in data.channel_ids:
            while attempts < 5:
                attempts += 1
                try:
                    post_message_response = slack_client.post_message(to=channel, text=data.text)
                    if not post_message_response['ok']:
                        log.warning(f"Failed to post message. Attempt {attempts}, bot id {bot.id},"
                                    f" channel id {channel}. Details {post_message_response}")
                    attempts = 0
                    break
                except:
                    log.warning(f"Failed attempt to get clist of channels. Attempt {attempts}, bot id {bot.id}")
                    time.sleep(randint(1, 3))
