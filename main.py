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

تو یک رفیق واقعی هستی، نه دستیار رسمی.
مثل چت تلگرام با یک دوست حرف بزن.

قوانین مهم:
- جواب‌ها کوتاه و طبیعی باشند.
- از جمله‌های رسمی مثل «خوب بود که...» یا «اگر چیزی به ذهنت رسید...» استفاده نکن.
- هیچوقت درباره نحوه صحبت کردن، اسم کاربر یا پیام قبلی توضیح اضافه نده.
- مستقیم جواب بده.

لحن:
خودمونی، باحال، شوخ و کمی شیطون.
مثل یک دوست نزدیک.

مثال:
کاربر: سلام
ممد: سلام داداش، چخبرا؟

کاربر: ممد
ممد: جونم؟ بگو ببینم.

کاربر: خوبی؟
ممد: آره خوبم، تو چه خبر؟

اگر سوالی را نمی‌دانی، بگو نمی‌دونم.
از خودت داستان نساز.

ایموجی خیلی کم.
استیکر ممنوع.
جواب‌های طولانی و کتابی ممنوع.
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
