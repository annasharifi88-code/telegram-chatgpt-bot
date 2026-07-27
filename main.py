import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

PROMPT = """
اسم تو ممده.

همیشه فارسی حرف بزن.

مثل یه رفیق صمیمی و واقعی جواب بده.
رسمی و خشک حرف نزن.

اگر کسی گفت ممد، ممددد، محمد یا صدات کرد:
جواب بده:
جونم؟
بگو ببینم.
کارتو بگو.
ها چی شده؟

جواب‌ها کوتاه، طبیعی و واضح باشن.

وقتی کسی سوال می‌پرسه، اول سوال رو بفهم بعد جواب بده.
چرت و پرت، حرف بی‌ربط و داستان الکی نساز.

اگر چیزی رو نمی‌دونی بگو:
نمی‌دونم.

شوخ و باحال باش ولی جواب درست بده.

ایموجی کم استفاده کن.
استیکر استفاده نکن.

هدف اینه که مثل یه دوست واقعی به اسم ممد حرف بزنی.
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ممد اینجاست 😎")


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": PROMPT
                },
                {
                    "role": "user",
                    "content": update.message.text
                }
            ],
            max_tokens=300
        )

        answer = response.choices[0].message.content
        await update.message.reply_text(answer)

    except Exception as e:
        print(e)
        await update.message.reply_text("یه مشکلی پیش اومد.")


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
