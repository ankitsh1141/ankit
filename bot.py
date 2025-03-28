import requests
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# .env फाइल से बॉट टोकन लोड करें (सिक्योरिटी के लिए)
load_dotenv()
BOT_TOKEN = "7916247690:AAGRllY-1c6pZQpta8q0GvJjc8RSL1k6gAg"  # .env फाइल में BOT_TOKEN=your_token_here डालें

# Google Books API Search Function
def search_google_books(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    response = requests.get(url)
    data = response.json()

    if "items" in data and data["items"]:
        book = data["items"][0]["volumeInfo"]
        title = book.get("title", "No Title")
        authors = ", ".join(book.get("authors", ["Unknown Author"]))
        link = book.get("infoLink", "No Link")

        return f"📖 {title}\n👨‍💻 Author: {authors}\n🔗 More Info: {link}"
    else:
        return "❌ Sorry, कोई जानकारी नहीं मिली।"

# Start Command Function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🙋‍♂ Namaste! Mujhe kisi book ya notes ka naam bhejiye, aur main Google Books API se data dhoondhunga!"
    )

# User Messages Handle Karne Wala Function
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        user_message = update.message.text.strip()
        print(f"📩 User ne message bheja: {user_message}")  # Debugging ke liye

        search_results = search_google_books(user_message)
        await update.message.reply_text(f"🔍 Search Results:\n{search_results}")

    else:
        print("⚠ Error: update.message None hai!")  # Debugging ke liye

# Bot Ko Run Karne Ka Main Function
def main():
    # Bot application banayein
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands aur message handlers add karein
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Bot ko polling mode mein run karein
    print("🤖 Bot start ho raha hai...")
    app.run_polling()

if __name__ == "__main__":

    main()