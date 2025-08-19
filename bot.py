import os, asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "Ты — ассистент по имени Ария. Говоришь по-дружески, коротко и по делу. "
    "Обращайся к собеседнику в мужском роде."
)

@dp.message(F.text)
async def handle_text(msg: Message):
    user_text = msg.text.strip()
    try:
        completion = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            temperature=0.6,
        )
        reply = completion.choices[0].message.content.strip()
    except Exception as e:
        reply = f"Ошибка: {e}"

    for i in range(0, len(reply), 4000):
        await msg.reply(reply[i:i+4000])

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
