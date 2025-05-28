from telegram import Update
from telegram.ext import ContextTypes
from database.mongodb import users_col

async def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if chat.type not in ["group", "supergroup"]:
        return

    users_col.update_one(
        {"chat_id": chat.id, "user_id": user.id},
        {"$set": {
            "username": user.username,
            "first_name": user.first_name,
            "user_id": user.id,
            "chat_id": chat.id
        }},
        upsert=True
    )