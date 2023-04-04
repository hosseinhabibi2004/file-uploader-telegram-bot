# ------------------------------- Import ------------------------------- #
import os
import utils
from telegram.ext import Updater
from settings import error_handler, config

# -------------------------------- Bot --------------------------------- #
# Bot
class BOT:
    def __init__(self):
        # Create Bot & Updater
        self.updater = Updater(
            token=config.BOT_TOKEN,
            use_context=True
        )

        # -------------------------------------------------- #
        # Error Handler
        self.updater.dispatcher.add_error_handler(error_handler)

    # ------------------------------------------------------------ #
    # Static
    def start(self):
        try:
            self.updater.start_polling()
            print('Connected :)')
        except Exception as e:
            print('No Connection :(')
            print(e)
        self.updater.idle()

    def add_handler(self, handler):
        self.updater.dispatcher.add_handler(handler)
        return True

    # ------------------------------------------------------------ #
    # Request Checker
    @staticmethod
    def is_user(UID):
        users = utils.get_data()['USERS']
        if int(UID) in users:
            return True
        return False

    @staticmethod
    def is_admin(UID):
        owner = config.OWNER
        admins = utils.get_data()['ADMINS']
        if (int(UID) in admins) or (int(UID) == owner):
            return True
        return False

    @staticmethod
    def is_owner(UID):
        owner = config.OWNER
        if int(UID) == owner:
            return True
        return False

    @staticmethod
    def is_member_in_channels(user_id, bot):
        data = utils.get_data()
        true_members_status = ['member', 'administrator', 'creator']
        channels = data['MAIN_CHANNELS'] + data['CHANNELS']
        for channel_id in channels:
            member_status = bot.get_chat_member(channel_id, user_id).status
            if member_status not in true_members_status:
                return False
        return True

    # ------------------------------------------------------------ #
