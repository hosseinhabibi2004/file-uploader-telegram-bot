# ------------------------------- Import ------------------------------- #
import json
from telegram.ext import MessageHandler, Filters, ConversationHandler, CommandHandler, ChatMemberHandler
from telegram import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB, ParseMode, ChatInviteLink, TelegramError
from telegram.utils.helpers import create_deep_linked_url

from settings import config
import utils
from . import BOT, button as btn, text as txt
from time import sleep
import os


# ---------------------------- File Uploader --------------------------- #
class FileUploader(BOT):
    def __init__(self):
        # Handlers
        self.MESSAGE = range(1)

        self.handlers = [
            ChatMemberHandler(self.chat_member_handler, ChatMemberHandler.ANY_CHAT_MEMBER),
            CommandHandler(txt.start_cmd, self.start_file, Filters.regex(txt.start_file_regex)),
            CommandHandler(txt.start_cmd, self.start_bot),
            CommandHandler(txt.backup_cmd, self.backup_data),
            CommandHandler(txt.channel_data_cmd, self.edit_channel_data),
            CommandHandler(txt.admin_data_cmd, self.edit_admin_data),
            MessageHandler(
                Filters.chat_type.private and Filters.document, self.add_file
            ),
            ConversationHandler(
                entry_points=[
                    CommandHandler(txt.send_all_cmd, self.get_message),
                ],
                states={
                    self.MESSAGE: [
                        MessageHandler(
                            Filters.all and ~Filters.command(txt.cancel_cmd), self.send_all
                        )
                    ],
                },
                fallbacks=[
                    CommandHandler(txt.cancel_cmd, self.cancel),
                ]
            ),
        ]

    # ------------------------------------------------------------ #
    # Static
    def backup_data(self, update, context):
        with open(os.path.join(config.BASE_DIR, "data.json"), "r") as data_file:
            context.bot.send_document(
                chat_id=config.OWNER, document=data_file, parse_mode=ParseMode.HTML
            )

    def cancel(self, update, context):
        CID = update.effective_chat.id
        text = txt.back_menu
        context.bot.send_message(CID, text)
        return ConversationHandler.END

    # ------------------------------------------------------------ #
    # Chat Member Handler
    def chat_member_handler(self, update, context):
        UID = update.effective_user.id
        data = utils.get_data()
        users = data['USERS']

        status = update.my_chat_member.new_chat_member.status
        if status == 'kicked':
            users.remove(str(UID))
        elif status == 'member':
            users.add(str(UID))
        else:
            text = f'[ChatMemberHandler]\n<code>{str(update)}</code>'
            return context.bot.send_message(
                config.OWNER, text, parse_mode=ParseMode.HTML, disable_web_page_preview=True
            )

        utils.update_data(data)

    # ------------------------------------------------------------ #
    # Start Bot
    def start_bot(self, update, context):
        UID = update.effective_user.id

        data = utils.get_data()
        if not self.is_user(UID):
            data['USERS'].add(str(UID))
        utils.update_data(data)

        text = txt.start_bot_text
        context.bot.send_message(
            UID, text, parse_mode=ParseMode.HTML, disable_web_page_preview=True
        )

    # ------------------------------------------------------------ #
    # Start File
    def start_file(self, update, context):
        UID = update.effective_user.id
        FID = update.message.text.replace(f"/{txt.start_cmd} file_", "")
        MID = update.message.message_id

        data = utils.get_data()
        if not self.is_user(UID):
            data['USERS'].add(str(UID))

        files = data['FILES']
        channels = self.is_member_in_channels(UID, context.bot)
        if channels == []:
            file = files[FID]
            if self.is_admin(UID):
                text = f"تعداد دانلود: {len(file['users'])}\n"
            else:
                if UID not in file['users']:
                    file['users'].add(str(UID))
                for channel in data['CHANNELS']:
                    if UID not in data['CHANNELS'][channel]['users']:
                        data['CHANNELS'][channel].add(str(UID))
                text = txt.bot_text
            context.bot.send_document(
                chat_id=UID, document=file['file_id'], caption=text, reply_to_message_id=MID, parse_mode=ParseMode.HTML
            )
        else:
            keyboard = []
            for channel_id, invite_link in channels.items():
                try:
                    channel = context.bot.get_chat(channel_id)
                    keyboard.append(
                        [IKB(text=channel.title, url=invite_link)]
                    )
                except Exception as e:
                    context.bot.send_message(
                        config.OWNER, f'[ERROR] (Get File)\n<a href="{create_deep_linked_url(context.bot.username, f"file_{FID}")}">File</a>\n\n{e}', parse_mode=ParseMode.HTML, disable_web_page_preview=True
                    )
            keyboard.append([IKB(text='📁 دریافت فایل 📁', url=create_deep_linked_url(context.bot.username, f"file_{FID}"))])
            text = txt.start_file_text.format(url=create_deep_linked_url(context.bot.username, f"file_{FID}"))
            context.bot.send_message(UID, text, reply_markup=IKM(keyboard), parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        utils.update_data(data)

    # ------------------------------------------------------------ #
    # Add File
    def add_file(self, update, context):
        UID = update.effective_user.id
        data = utils.get_data()
        files = data['FILES']

        document = update.message.document
        if document.file_unique_id not in files:
            files[document.file_unique_id] = {
                'file_id': document.file_id,
                'users': list()
            }
        utils.update_data(data)
        self.backup_data(update, context)

        text = create_deep_linked_url(context.bot.username, f"file_{document.file_unique_id}")
        context.bot.send_message(
            UID, text, parse_mode=ParseMode.HTML, disable_web_page_preview=True
        )

    # ------------------------------------------------------------ #
    # Channel Data
    def edit_channel_data(self, update, context):
        UID = update.effective_user.id
        channel_data = update.message.text.replace(f'/{txt.channel_data_cmd} ', '').split(' ')

        data = utils.get_data()
        channels = data['CHANNELS']
        if self.is_admin(UID):
            if channel_data[0] == f'/{txt.channel_data_cmd}':
                send_to = UID
                text = 'کانال های فعلی\n\n'
                for channel_id in channels:
                    try:
                        channel = context.bot.get_chat(channel_id)
                        if channel.invite_link != None:
                            text += f'✅ <a href="{channel.invite_link}">{channel.title}</a>\n#️⃣ {len(channels[str(channel.id)]["users"])}\n\n'
                        else:
                            text += f'❌ <a href="https://t.me/{channel.username}">{channel.title}</a>\n#️⃣ {len(channels[str(channel.id)]["users"])}\n\n'
                    except Exception as e:
                        context.bot.send_message(
                            config.OWNER, f"{channel_id}\n<code>{e}</code>", parse_mode=ParseMode.HTML, disable_web_page_preview=True
                        )
            else:
                try:
                    if channel_data[0].replace('-', '').isdigit():
                        if not channel_data[0].startswith('-100'):
                            channel_data[0] = '-100' + channel_data[0]
                    else:
                        if '/' in channel_data[0]:
                            channel_data[0] = channel_data[0].split('/')[-1]
                        if not channel_data[0].startswith('@'):
                            channel_data[0] = '@' + channel_data[0]

                    channel = context.bot.get_chat(channel_data[0])
                    if channel.type in ['group', 'supergroup', 'channel']:
                        if str(channel.id) not in channels:
                            if len(channel_data) == 2:
                                new_invite_link = channel.create_invite_link(name=config.TG_NAME, member_limit=int(channel_data[1])).invite_link
                                channels[str(channel.id)] = {'invite_link': new_invite_link, 'users': list()}
                            else:
                                new_invite_link = channel.revoke_invite_link(channel.invite_link).invite_link
                                channels[str(channel.id)] = {'invite_link': None, 'users': list()}
                            send_to = UID
                            text = f'✅ چنل <b>{channel.title}</b> اضافه شد.'
                        else:
                            del channels[str(channel.id)]
                            send_to = UID
                            text = f'❌ چنل <b>{channel.title}</b> حذف شد.'
                        utils.update_data(data)
                        self.backup_data(update, context)
                    else:
                        send_to = UID
                        text = 'ورودی نامعتبر.'
                except Exception as e:
                    if str(e) == 'Chat not found':
                        send_to = UID
                        text = "ربات در چنل عضو نیست."
                    elif str(e) == 'Not enough rights to manage chat invite link':
                        send_to = UID
                        text = "ربات دسترسی کافی را ندارد."
                    else:
                        send_to = config.OWNER
                        text = f'[COMMAND]\n{update.message.text}\n\n[ERROR]\n{str(e)}'

            return context.bot.send_message(
                send_to, text, parse_mode=ParseMode.HTML, disable_web_page_preview=True
            )

    # ------------------------------------------------------------ #
    # Admin Data
    def edit_admin_data(self, update, context):
        UID = update.effective_user.id
        user_data = update.message.text.replace(f'/{txt.admin_data_cmd} ', '')

        data = utils.get_data()
        admins = data['ADMINS']
        if self.is_owner(UID):
            if user_data == f'/{txt.admin_data_cmd}':
                text = 'ادمین‌ها\n\n'
                for admin_id in admins:
                    admin = context.bot.get_chat(admin_id)
                    text += f'<a href="https://t.me/{admin.username}">{admin.first_name if admin.first_name != None else ""} {admin.last_name if admin.last_name != None else ""}</a>\n'
            else:
                if not user_data.isdigit():
                    if '/' in user_data:
                        user_data = user_data.split('/')[-1]
                    if not user_data.startswith('@'):
                        user_data = '@' + user_data

                try:
                    user = context.bot.get_chat(user_data)
                    if user.type == 'private':
                        if str(user.id) not in admins:
                            admins.add(str(user.id))
                            text = f'✅ کاربر <b>{user.first_name if user.first_name != None else ""} {user.last_name if user.last_name != None else ""}</b> ادمین شد.'
                        else:
                            admins.remove(str(user.id))
                            text = f'❌ کاربر <b>{user.first_name if user.first_name != None else ""} {user.last_name if user.last_name != None else ""}</b> از لیست ادمین‌ها حذف شد.'
                        utils.update_data(data)
                        self.backup_data(update, context)
                    else:
                        text = 'ورودی نامعتبر.'
                except Exception as e:
                    text = f'[COMMAND]\n{update.message.text}\n\n[ERROR]\n{str(e)}'

            return context.bot.send_message(
                UID, text, parse_mode=ParseMode.HTML, disable_web_page_preview=True
            )

    # ------------------------------------------------------------ #
    # Send All
    def get_message(self, update, context):
        UID = update.effective_user.id
        if self.is_admin(UID):
            text = txt.get_message
            context.bot.send_message(UID, text)
            return self.MESSAGE

    def send_all(self, update, context):
        UID = update.effective_user.id
        users = utils.get_data()['USERS']

        sended_count, error_count = 0, 0
        for user_id in users:
            try:
                context.bot.copy_message(user_id, UID, update.message.message_id, parse_mode=ParseMode.HTML)
                sended_count += 1
            except Exception as e:
                context.bot.send_message(
                    config.OWNER, f"[ERROR] (Send All)\n{e}", parse_mode=ParseMode.HTML, disable_web_page_preview=True
                )
                error_count += 1
            sleep(0.5)

        text = f"ارسال پیام به کاربران به اتمام رسید.\n✅ تعداد نفرات ارسال شده : {sended_count}\n❌ تعداد نفرات ارسال نشده : {error_count}"
        context.bot.send_message(
            UID, text, parse_mode=ParseMode.HTML, disable_web_page_preview=True
        )
        return ConversationHandler.END
