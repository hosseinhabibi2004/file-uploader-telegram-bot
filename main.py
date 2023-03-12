# ------------------------------- Import ------------------------------- #
from Telegram import BOT
from Telegram.file_uploader import FileUploader


# -------------------------------- Main -------------------------------- #
def main():
    # -------------------------------------------------- #
    # BOT Settings
    bot = BOT()

    # -------------------------------------------------- #
    # ADD HANDLERS
    file_uploader_bot = FileUploader()
    for handler in file_uploader_bot.handlers:
        bot.add_handler(handler)

    bot.start()


if __name__ == '__main__':
    main()
