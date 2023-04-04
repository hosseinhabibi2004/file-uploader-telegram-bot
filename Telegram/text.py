# ------------------------------- Import ------------------------------- #
from settings import config

# -------------------------------- Regex ------------------------------- #
date_regex = r"^(([1][3-4]\d{2})-((0[1-6]-((3[0-1])|([1-2][0-9])|(0[1-9])))|((1[0-2]|(0[7-9]))-(30|31|([1-2][0-9])|(0[1-9])))))$"
number_regex = r"^([\d]+)$"
start_file_regex = r"^(/start file_[a-zA-Z0-9-_]+)$"

# ------------------------------- Command ------------------------------ #
start_cmd = "start"
backup_cmd = "backup"
cancel_cmd = "cancel"
channel_data_cmd = "channel"
admin_data_cmd = "admin"
send_all_cmd = "all"

# -------------------------------- Text -------------------------------- #
# Variables
bot_text = '➢ ' + config.TG_ID

start_bot_text = f'سلام، به ربات آپلودر {config.TG_NAME} خوش اومدید.'

start_file_text = 'جهت دریافت فایل، لطفاً در کانال های زیر عضو شوید.\n\n پس از عضویت <a href="{url}">اینجا</a> کلیک کنید.'

back_menu = "با موفقیت به منو بازگشتید."

cancel = f"\nبرای لغوکردن میتوانید از « /{cancel_cmd} » استفاده کنید."

get_message = "لطفاً متن مورد نظر را ارسال کنید." + cancel


# ------------------------------------------------------------ #
# Functions
