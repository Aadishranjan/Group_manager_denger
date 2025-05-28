from telegram import Update
from telegram.ext import ContextTypes
from database.mongodb import users_col
from config import BOT_OWNER_ID
BOT_OWNER_ID = int(BOT_OWNER_ID)
print(BOT_OWNER_ID)

async def ban_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != BOT_OWNER_ID:
        return await update.message.reply_text("You are not authorized to use this command.")

    # Get chat_id (target group) from command args
    args = context.args
    if not args:
        return await update.message.reply_text("Usage: /banall <chat_id>")
    
    chat_id = int(args[0])
    bot = context.bot

    try:
        # Get list of admins in the group
        admins = await bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]

        # Fetch users from DB
        users = users_col.find({"chat_id": chat_id})

        count = 0
        for user in users:
            user_id = user["user_id"]
            if user_id in admin_ids:
                continue  # Skip admins

            try:
                await bot.ban_chat_member(chat_id, user_id)
                count += 1
            except Exception as e:
                print(f"Failed to ban {user_id}: {e}")

        await update.message.reply_text(f"Banned {count} users from group {chat_id}.")

    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("An error occurred.")