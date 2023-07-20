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
        if str(UID) in users:
            return True
        return False

    @staticmethod
    def is_admin(UID):
        owner = config.OWNER
        admins = utils.get_data()['ADMINS']
        if (str(UID) in admins) or (str(UID) == owner):
            return True
        return False

    @staticmethod
    def is_owner(UID):
        owner = config.OWNER
        if str(UID) == owner:
            return True
        return False

    def is_member_in_channels(self, user_id, bot):
        not_joined_channels = dict()
        data = utils.get_data()
        true_members_status = ['member', 'administrator', 'creator']

        if not self.is_admin(user_id):
            for channel_id in data['MAIN_CHANNELS']:
                try:
                    channel = bot.get_chat(channel_id)
                    invite_link = channel.invite_link

                    member_status = bot.get_chat_member(channel_id, user_id).status
                    if member_status not in true_members_status:
                        not_joined_channels[channel_id] = invite_link
                except:
                    pass

            for channel_id in data['CHANNELS']:
                try:
                    if data['CHANNELS'][channel_id]['invite_link'] == None:
                        channel = bot.get_chat(channel_id)
                        invite_link = channel.invite_link
                    else:
                        invite_link = data['CHANNELS'][channel_id]['invite_link']

                    member_status = bot.get_chat_member(channel_id, user_id).status
                    if member_status not in true_members_status:
                        not_joined_channels[channel_id] = invite_link
                except Exception as e:
                    print(1, e)
        return not_joined_channels

    # ------------------------------------------------------------ #
