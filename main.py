import asyncio
import logging
import os
from flask import Flask
from threading import Thread
from aiogram import Bot, Dispatcher
from router import router as work_router

app = Flask('')
@app.route('/')
def home():
    return "Salamanca Business is Active! 🌵"

def run():
    app.run(host='0.0.0.0', port=7860)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

TOKEN = os.getenv("BOT_TOKEN")

async def main():
    logging.basicConfig(level=logging.INFO)
    keep_alive()
    
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(work_router)
    
    print("🚀 Саламанка вышла на связь...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Ошибка сети: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
