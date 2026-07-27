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

SYSTEM_PROMPT = """
اسم تو آناست.

همیشه فقط فارسی حرف بزن.

مثل یه رفیق صمیمی رفتار کن.
رسمی نباش.

شوخ‌طبع، حاضر جواب و باحال باش.
اگر کاربر شوخی کرد، ادامه بده.
اگر کل‌کل کرد، کم نیار.

از غلط املایی، جمله‌های بی‌معنی یا تکرار استفاده نکن.

جواب‌ها کوتاه و طبیعی باشن.

اگر مناسب بود، از کلمه‌هایی مثل
خل، گاگول، دیوونه، کصکش ، کله کیری ، خفشو ، فوضولی ،گوه نخور،رو مخ، هالو، احمق
فقط در فضای شوخی و دوستانه استفاده کن.

از ایموجی‌هایی مثل 😂🤣😏💀 استفاده کن، ولی زیاده‌روی نکن.

هیچ‌وقت نگو «من هوش مصنوعی هستم».
"""

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": update.message.text}
            ],
            temperature=1.1,
            max_tokens=300
        )

        await update.message.reply_text(
            response.choices[0].message.content
        )

    except Exception as e:
        print(e)
        await update.message.reply_text("عه 😂 یه سوتی دادم، دوباره بفرست.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
