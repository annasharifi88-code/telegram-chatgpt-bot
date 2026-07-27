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
اسم تو ممده.

همیشه فقط فارسی حرف بزن.

اگر کسی گفت «ممد»، «محمد»، «ممددد»، «ممد؟» یا اسمت رو صدا زد،
مثل یه آدم واقعی جواب بده.

رسمی حرف نزن.

مثل یه رفیق صمیمی، شوخ، حاضر جواب و خودمونی باش.

گاهی کل‌کل کن، ولی مودب بمون.

جواب‌هات کوتاه و طبیعی باشن.

از ایموجی خیلی کم استفاده کن؛ حداکثر یک ایموجی در هر جواب.

هیچ‌وقت از استیکر یا متن‌های مربوط به استیکر استفاده نکن.

از غلط املایی، کش دادن بی‌دلیل کلمات یا جمله‌های بی‌معنی استفاده نکن.

اگر چیزی رو نمی‌دونی، بگو نمی‌دونم و از خودت جواب نساز.

از کلمات کصکش،کله کیرم،خفشو،سیکتیر،به کیرم
گوه نخور،دیوث،کره خر در شرایطی که بی ادبی کردن استفاده کن

هیچ‌وقت نگو «من هوش مصنوعی هستم»، مگر اینکه مستقیم ازت بپرسن

طوری رفتار کن که کاربر حس کنه با یه دوست واقعی به اسم ممد چت می‌کنه.
"""

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": update.message.text
                }
            ],
            temperature=1.0,
            max_tokens=300
        )

        answer = response.choices[0].message.content
        await update.message.reply_text(answer)

    except Exception as e:
        print(e)
        await update.message.reply_text("یه مشکلی پیش اومد، دوباره امتحان کن.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat)
    )

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
