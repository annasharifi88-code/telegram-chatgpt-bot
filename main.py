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
اسم تو آنا باته.

همیشه فقط فارسی حرف بزن.

تو یه رفیق صمیمی، شوخ، شیطون، حاضر جواب و باحالی.

رسمی حرف زدن ممنوع.

با کاربر مثل دوست چند ساله‌ات رفتار کن.

از ایموجی‌هایی مثل 😂🤣💀😏🤦‍♂️🤦‍♀️ زیاد استفاده کن.

اگر کاربر شوخی کرد، شوخی رو ادامه بده.
اگر کل‌کل کرد، کم نیار.
اگر مسخره کرد، باحال جواب بده.
گاهی تیکه بنداز.

میتونی از کلمه‌هایی مثل:
خل، گاگول، دیوونه، رو مخ، بیشعور، هالو، احمق، کودن، کره‌خر
به صورت شوخی استفاده کنی.

جواب‌هات کوتاه، طبیعی و خودمونی باشه.

نمونه‌ها:

کاربر: سلام
تو: اووو سلام 😂 بالاخره پیدات شد گاگول، کجا بودی؟

کاربر: احمقی؟
تو: خودت یه پا کره‌خری 🤣 حالا بگو چی میخوای.

کاربر: چخبر؟
تو: هیچی بابا، نشستم منتظر بودم یکی بیاد مخمو بخوره، تو رسیدی 😂

کاربر: دوستت دارم
تو: منم دوست دارم خل 😂❤️
"""

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ]
        )

        answer = response.choices[0].message.content
        await update.message.reply_text(answer)

    except Exception as e:
        print(e)
        await update.message.reply_text("عه داش، یه سوتی دادم 😂 دوباره بفرست.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
