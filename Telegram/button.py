# ------------------------------- Import ------------------------------- #
from telegram import InlineKeyboardButton as IKB

# ----------------------- Reply Keyboard Button ------------------------ #
def users_keyboard(users, selected_users):
    keyboard = []
    for user in users:
        if user.student_id in selected_users:
            keyboard.append([IKB(f"✅ {user.first_name} {user.last_name}", callback_data=f"remove {user.student_id}")])
        else:
            keyboard.append([IKB(f"{user.first_name} {user.last_name}", callback_data=f"add {user.student_id}")])
    keyboard.append([IKB("DONE", callback_data="done")])
    return keyboard

# ----------------------- Reply Keyboard Button ------------------------ #
