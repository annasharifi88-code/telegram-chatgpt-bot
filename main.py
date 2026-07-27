import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "تو یک دستیار فارسی‌زبان، دوستانه و باهوش هستی. همیشه به فارسی جواب بده."
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )

        answer = response.choices[0].message.content
        await update.message.reply_text(answer)

    except Exception as e:
        print(e)
        await update.message.reply_text(f"خطا: {e}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
