import os
import asyncio
import json
from aiogram import Router, F, Bot
from aiogram.types import (
    Message, FSInputFile, CallbackQuery,
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender

# Импорт твоих скриптов
from downloader import download_video
from audio_downloader import download_audio

router = Router()

url_storage = {}
user_langs = {}

# Статистика (пишем в /tmp, чтобы Render не ругался)
DB_FILE = "/tmp/stats.json"

def update_stats(user_id, is_download=False):
    try:
        if not os.path.exists(DB_FILE):
            data = {"users": [], "total_downloads": 0}
        else:
            with open(DB_FILE, "r") as f:
                data = json.load(f)

        if str(user_id) not in [str(u) for u in data["users"]]:
            data["users"].append(user_id)

        if is_download:
            data["total_downloads"] += 1

        with open(DB_FILE, "w") as f:
            json.dump(data, f)
    except:
        pass

# Настройки каналов и админов
CHANNELS = ["@Iskandar_Tg10"]
ADMINS = [821943413]

async def check_sub(bot: Bot, user_id: int):
    if user_id in ADMINS:
        return True
    for ch_id in CHANNELS:
        try:
            m = await bot.get_chat_member(chat_id=ch_id, user_id=user_id)
            if m.status in ["member", "administrator", "creator"]:
                return True
        except:
            continue
    return False

# Твои тексты (Полный боекомплект)
TEXTS = {
    "uzb": {
        "start": "👋 <b>Assalomu alaykum!</b>\n\nMen TikTok, Instagram va YouTube-dan videolarni yuklayman 📥, shuningdek ularni <b>MP3 audio</b> formatiga o'girib beraman! 🎵✨\n\n🚀 <b>Boshlash uchun video havolasini yuboring!</b> 🔗⬇️",
        "sub": "🔒 <b>Botdan foydalanish uchun kanalimizga obuna bo'ling:</b> 📢👇",
        "error": "❌ <b>Xatolik!</b>\nHavola noto'g'ri yoki YouTube bizni blokladi. 🚫🛰",
        "about": "🤖 <b>YtsSaveBot v2.0</b>\n\nBu shunchaki bot emas — bu sizning media-yordamchingiz! 🔥💎\n\n👑 <b>Admin:</b> @Iskandar_Hzd10\n📢 <b>Kanal:</b> @Iskandar_Tg10",
        "inst": "📖 <b>Yo'riqnoma:</b>\n\n1️⃣ Linkni nusxalang 🖇.\n2️⃣ Botga yuboring 📤.\n3️⃣ Formatni tanlang! 🚀",
        "help": "🆘 <b>Yordam markazi</b>\n\nAdmin: @Iskandar_Hzd10 🛡",
        "choose": "📥 <b>Formatni tanlang:</b>",
        "v_btn": "🎬 Video (MP4)",
        "a_btn": "🎧 Audio (MP3)",
        "loading": "⌛ <b>Yuklanmoqda... Kuting...</b>"
    },
    "rus": {
        "start": "👋 <b>Приветствую!</b>\n\nЯ качаю видео из TikTok, Instagram и YouTube 📥, а также умею делать <b>MP3!</b> 🎵✨\n\n🚀 <b>Просто отправь мне ссылку!</b> 🔗⬇️",
        "sub": "🔒 <b>Для использования бота подпишитесь на канал:</b> 📢👇",
        "error": "❌ <b>Ошибка!</b>\nПроверьте ссылку или YouTube блокирует сервер. 🚫🛰",
        "about": "🤖 <b>YtsSaveBot v2.0</b>\n\nЛичный медиа-комбайн Семьи Саламанка! 🔥💎\n👑 <b>Автор:</b> @Iskandar_Hzd10\n📢 <b>Канал:</b> @Iskandar_Tg10",
        "inst": "📖 <b>Инструкция:</b>\n\n1️⃣ Скопируй ссылку 🖇.\n2️⃣ Отправь боту 📤.\n3️⃣ Выбери Видео или MP3! 🚀",
        "help": "🆘 <b>Поддержка</b>\n\nАдмин: @Iskandar_Hzd10 🛡",
        "choose": "📥 <b>Выберите формат:</b>",
        "v_btn": "🎬 Видео (MP4)",
        "a_btn": "🎧 Аудио (MP3)",
        "loading": "⌛ <b>Загрузка... Жди...</b>"
    },
    "eng": {
        "start": "👋 <b>Welcome!</b>\n\nI download videos from TikTok, Instagram, and YouTube 📥, and MP3 too! 🎵✨\n\n🚀 <b>Just send me a video link!</b> 🔗⬇️",
        "sub": "🔒 <b>Please subscribe to our channel to use the bot:</b> 📢👇",
        "error": "❌ <b>Error!</b>\nIncorrect link or YouTube block. 🚫🛰",
        "about": "🤖 <b>YtsSaveBot v2.0</b>\nUltimate media assistant! 🔥💎\n👑 <b>Owner:</b> @Iskandar_Hzd10\n📢 <b>Channel:</b> @Iskandar_Tg10",
        "inst": "📖 <b>User Guide:</b>\n1️⃣ Copy link 🖇. 2️⃣ Send here 📤. 3️⃣ Choose format! 🚀",
        "help": "🆘 <b>Support Center</b>\nAdmin: @Iskandar_Hzd10 🛡",
        "choose": "📥 <b>Choose format:</b>",
        "v_btn": "🎬 Video (MP4)",
        "a_btn": "🎧 Audio (MP3)",
        "loading": "⌛ <b>Loading... Wait...</b>"
    }
}

# Клавиатуры
def get_main_kb(lang):
    btns = {
        "uzb": ["⚙️ Sozlamalar", "👤 Bot haqida", "📖 Ko'rsatma"],
        "rus": ["⚙️ Настройки", "👤 О боте", "📖 Инструкция"],
        "eng": ["⚙️ Settings", "👤 About", "📖 Instruction"]
    }
    b = btns[lang]
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=b[0]), KeyboardButton(text=b[1])],
            [KeyboardButton(text=b[2])]
        ],
        resize_keyboard=True
    )

def get_sub_kb(lang):
    text = "Tekshirish ✅" if lang == "uzb" else "Check ✅" if lang == "eng" else "Проверить ✅"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Iskandar Football ⚽️", url="https://t.me/Iskandar_Tg10")],
        [InlineKeyboardButton(text=text, callback_data=f"check_sub_{lang}")]
    ])

# Хендлеры
@router.message(Command("start"))
@router.message(Command("lang"))
async def cmd_start_lang(message: Message):
    update_stats(message.from_user.id)
    await message.answer(
        "🇺🇿 Tilni tanlang / 🇷🇺 Выберите язык / 🇺🇸 Choose language 🌐",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="sl_uzb")],
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="sl_rus")],
            [InlineKeyboardButton(text="🇺🇸 English", callback_data="sl_eng")]
        ])
    )

@router.callback_query(F.data.startswith("sl_"))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    user_langs[callback.from_user.id] = lang
    await callback.message.delete()
    await callback.message.answer(TEXTS[lang]["start"], reply_markup=get_main_kb(lang), parse_mode="HTML")

@router.callback_query(F.data.startswith("check_sub_"))
async def sub_callback(callback: CallbackQuery, bot: Bot):
    lang = callback.data.split("_")[-1]
    if await check_sub(bot, callback.from_user.id):
        await callback.message.delete()
        await callback.message.answer(TEXTS[lang]["start"], reply_markup=get_main_kb(lang), parse_mode="HTML")
    else:
        msg = "Obuna bo'ling! ❌" if lang == "uzb" else "Subscribe! ❌" if lang == "eng" else "Подпишитесь! ❌"
        await callback.answer(msg, show_alert=True)

@router.message(F.text.contains("http"))
async def handle_link(message: Message, bot: Bot):
    user_lang = user_langs.get(message.from_user.id, "rus")
    if not await check_sub(bot, message.from_user.id):
        await message.answer(TEXTS[user_lang]["sub"], reply_markup=get_sub_kb(user_lang), parse_mode="HTML")
        return

    clean_url = message.text.strip().split("?")[0].split("&")[0]
    link_id = str(hash(clean_url))
    url_storage[link_id] = clean_url

    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=TEXTS[user_lang]["v_btn"], callback_data=f"dl_v_{user_lang}_{link_id}"),
        InlineKeyboardButton(text=TEXTS[user_lang]["a_btn"], callback_data=f"dl_a_{user_lang}_{link_id}")
    ]])

    await message.answer(TEXTS[user_lang]["choose"], reply_markup=kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("dl_"))
async def process_download(callback: CallbackQuery, bot: Bot):
    _, mode, lang, link_id = callback.data.split("_")
    url = url_storage.get(link_id)

    if not url:
        await callback.answer("❌ Error: Link expired", show_alert=True)
        return

    status_msg = await callback.message.answer(TEXTS[lang]["loading"], parse_mode="HTML")

    async with ChatActionSender(bot=bot, chat_id=callback.message.chat.id, action="upload_document"):
        # Запуск скачивания в отдельном потоке
        path = await asyncio.to_thread(download_video if mode == "v" else download_audio, url)

        if path and os.path.exists(path):
            try:
                await status_msg.delete()
                file = FSInputFile(path)
                caption = "✅ @YtsSave_Bot ✨"

                if mode == "v":
                    await callback.message.answer_video(video=file, caption=caption)
                else:
                    await callback.message.answer_audio(audio=file, caption=caption)

                update_stats(callback.from_user.id, is_download=True)
            except Exception as e:
                await callback.message.answer(f"❌ Send Error: {e}")
            finally:
                if os.path.exists(path):
                    os.remove(path) # Чистим место
        else:
            await status_msg.edit_text(TEXTS[lang]["error"], parse_mode="HTML")

# Хендлеры кнопок меню
@router.message(F.text.in_(["⚙️ Настройки", "⚙️ Sozlamalar", "⚙️ Settings"]))
async def settings_h(message: Message):
    lang = user_langs.get(message.from_user.id, "rus")
    await message.answer(TEXTS[lang]["help"], parse_mode="HTML")

@router.message(F.text.in_(["👤 О боте", "👤 Bot haqida", "👤 About"]))
async def about_h(message: Message):
    lang = user_langs.get(message.from_user.id, "rus")
    await message.answer(TEXTS[lang]["about"], parse_mode="HTML")

@router.message(F.text.in_(["📖 Инструкция", "📖 Ko'rsatma", "📖 Instruction"]))
async def inst_h(message: Message):
    lang = user_langs.get(message.from_user.id, "rus")
    await message.answer(TEXTS[lang]["inst"], parse_mode="HTML")


# here adding a bot to chats of tg
# after gitting the oracle cloud acc
