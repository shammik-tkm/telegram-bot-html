import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)
from aiohttp import web
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Укажи BOT_TOKEN в .env файле")

# ==================== НАСТРОЙКИ ====================
ADMIN_ID = 7167734784
SEND_HOUR = 0
SEND_MINUTE = 0
TIMEZONE = "Asia/Kuala_Lumpur"  # GMT+8

DATA_FILE = Path("data.json")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone=TIMEZONE)

DEFAULT_DATA = {
    "day_index": 0,
    "current_assignments": {},
    "completed": {},
    "last_send_date": None,
    "users": [
        {"id": 6990139455, "name": "shammik_77", "username": "@shammik_77"},
        {"id": 1307640212, "name": "dude87fx", "username": "@dude87fx"},
        {"id": 6093086439, "name": "ronny_g7", "username": "@ronny_g7"},
        {"id": 1051291465, "name": "paaltayev", "username": "@paaltayev"},
        {"id": 1983522833, "name": "Atjnw", "username": "@Atjnw"},
        {"id": 6078576183, "name": "Незнаю", "username": "@ya_ctoto"},
    ],
    "tasks": [
        "🧹 Убрать комнату",
        "🗑️ Вынести мусор",
        "🍽️ Помыть посуду",
    ],
    "history": [],
    "send_hour": SEND_HOUR,
    "send_minute": SEND_MINUTE,
}

# ==================== ДАННЫЕ ====================

def load_data():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = DEFAULT_DATA.copy()
    else:
        data = DEFAULT_DATA.copy()

    for k, v in DEFAULT_DATA.items():
        data.setdefault(k, v)

    return data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID

def make_task_keyboard(user_id: str, tasks: list, completed: list):
    buttons = []
    for task in tasks:
        mark = "✅" if task in completed else "⬜"
        buttons.append([InlineKeyboardButton(
            text=f"{mark} {task}",
            callback_data=f"done:{user_id}:{task}"
        )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# ==================== АВТО-ОТПРАВКА В 00:00 ====================

async def send_daily_tasks(force: bool = False):
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")

    if not force and data.get("last_send_date") == today:
        return

    users = data.get("users", [])
    tasks = data.get("tasks", [])

    if not users or not tasks:
        await bot.send_message(ADMIN_ID, "⚠️ Список пользователей или задач пуст!")
        return

    day_index = data.get("day_index", 0)
    current_user = users[day_index % len(users)]
    uid_str = str(current_user["id"])

    assignments = {uid_str: tasks.copy()}

    if data.get("current_assignments") and data.get("last_send_date"):
        data["history"].append({
            "date": data["last_send_date"],
            "assignments": data["current_assignments"],
            "completed": data.get("completed", {})
        })
        data["history"] = data["history"][-30:]

    data["current_assignments"] = assignments
    data["completed"] = {uid_str: []}
    data["last_send_date"] = today
    data["day_index"] = day_index + 1
    save_data(data)

    text = (
        f"📅 <b>Задания на сегодня (00:00 Kuala Lumpur)</b>\n\n"
        f"Привет, {current_user['name']}!\n"
        f"Твои задания:\n\n"
    )
    for i, t in enumerate(tasks, 1):
        text += f"{i}. {t}\n"
        
    kb = make_task_keyboard(uid_str, tasks, [])

    try:
        await bot.send_message(current_user["id"], text, reply_markup=kb, parse_mode=ParseMode.HTML)
        await bot.send_message(
            ADMIN_ID,
            f"🚀 <b>Авто-отправка в 00:00 выполнена!</b>\n"
            f"Получатель: {current_user['username']} ({current_user['name']})",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        await bot.send_message(
            ADMIN_ID,
            f"⚠️ Ошибка отправки пользователю {current_user['name']}:\n<code>{e}</code>",
            parse_mode=ParseMode.HTML
        )

# ==================== API ДЛЯ HTML АДМИНКИ ====================

async def api_get_data(request):
    data = load_data()
    return web.json_response(data, headers={"Access-Control-Allow-Origin": "*"})

async def api_save_data(request):
    try:
        new_data = await request.json()
        
        # Перенастраиваем таймер, если изменили время из HTML
        data = load_data()
        if new_data.get("send_hour") != data.get("send_hour") or new_data.get("send_minute") != data.get("send_minute"):
            try:
                scheduler.remove_job("daily_tasks")
            except Exception:
                pass
            scheduler.add_job(
                send_daily_tasks,
                trigger="cron",
                hour=new_data["send_hour"],
                minute=new_data["send_minute"],
                id="daily_tasks"
            )

        save_data(new_data)
        return web.json_response({"status": "ok"}, headers={"Access-Control-Allow-Origin": "*"})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=400)

async def api_force_send(request):
    await send_daily_tasks(force=True)
    return web.json_response({"status": "ok"}, headers={"Access-Control-Allow-Origin": "*"})

async def api_options(request):
    return web.Response(headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "*"
    })

def setup_http_server():
    app = web.Application()
    app.router.add_get("/api/data", api_get_data)
    app.router.add_post("/api/data", api_save_data)
    app.router.add_post("/api/force", api_force_send)
    app.router.add_options("/api/{tail:.*}", api_options)
    return app

# ==================== ХЭНДЛЕРЫ BOT ====================

@dp.callback_query(F.data.startswith("done:"))
async def on_task_done(callback: CallbackQuery):
    parts = callback.data.split(":", 2)
    if len(parts) < 3: return
    _, uid_str, task = parts
    
    if str(callback.from_user.id) != uid_str:
        await callback.answer("Это не твоё задание!", show_alert=True)
        return

    data = load_data()
    completed = data.get("completed", {})
    if uid_str not in completed: completed[uid_str] = []

    if task in completed[uid_str]:
        completed[uid_str].remove(task)
        await callback.answer("Отметка снята")
    else:
        completed[uid_str].append(task)
        await callback.answer("Задание выполнено! 👏")
        await bot.send_message(ADMIN_ID, f"✅ {callback.from_user.username or uid_str} выполнил:\n{task}")

    data["completed"] = completed
    save_data(data)

    tasks = data["current_assignments"].get(uid_str, [])
    kb = make_task_keyboard(uid_str, tasks, completed[uid_str])
    try: await callback.message.edit_reply_markup(reply_markup=kb)
    except Exception: pass

# ==================== ЗАПУСК ====================

async def main():
    data = load_data()
    
    # Ставим авто-рассылку на 00:00 (Asia/Kuala_Lumpur)
    scheduler.add_job(
        send_daily_tasks,
        trigger="cron",
        hour=data.get("send_hour", SEND_HOUR),
        minute=data.get("send_minute", SEND_MINUTE),
        id="daily_tasks"
    )
    scheduler.start()

    # Запускаем API сервер на порту 8080
    app = setup_http_server()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

    print(f"Бот запущен. Авто-рассылка в {data['send_hour']:02d}:{data['send_minute']:02d} ({TIMEZONE})")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())