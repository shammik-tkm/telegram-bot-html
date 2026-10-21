import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
)
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Укажи BOT_TOKEN в .env файле")

# ==================== НАСТРОЙКИ ====================
ADMIN_ID = 7167734784

DEFAULT_USERS = [
    {"id": 6990139455, "name": "shammik_77", "username": "@shammik_77"},
    {"id": 1307640212, "name": "dude87fx", "username": "@dude87fx"},
    {"id": 6093086439, "name": "ronny_g7", "username": "@ronny_g7"},
    {"id": 1051291465, "name": "paaltayev", "username": "@paaltayev"},
    {"id": 1983522833, "name": "Atjnw", "username": "@Atjnw"},
    {"id": 6078576183, "name": "Незнаю", "username": "@ya_ctoto"},
]

DEFAULT_TASKS = [
    "🧹 Убрать комнату",
    "🗑️ Вынести мусор",
    "🍽️ Помыть посуду",
]

SEND_HOUR = 9
SEND_MINUTE = 0

DATA_FILE = Path("data.json")
# ===================================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone="Asia/Ashgabat")

# ==================== КЛАВИАТУРЫ ====================

def get_admin_keyboard():
    """Кнопки для админа"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📊 Статус"),
                KeyboardButton(text="🚀 Отправить сейчас"),
                KeyboardButton(text="🔮 Кто завтра"),
            ],
            [
                KeyboardButton(text="👥 Пользователи"),
                KeyboardButton(text="📝 Задания"),
                KeyboardButton(text="📜 История"),
            ],
            [
                KeyboardButton(text="📢 Рассылка"),
                KeyboardButton(text="🔄 Сброс"),
                KeyboardButton(text="⏰ Время"),
            ],
            [
                KeyboardButton(text="📋 Мои задания"),
                KeyboardButton(text="❓ Помощь"),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выбери действие..."
    )

def get_user_keyboard():
    """Кнопки для обычного пользователя"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📋 Мои задания"),
                KeyboardButton(text="❓ Помощь"),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выбери действие..."
    )

# ==================== ДАННЫЕ ====================

def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    data.setdefault("day_index", 0)
    data.setdefault("current_assignments", {})
    data.setdefault("completed", {})
    data.setdefault("last_send_date", None)
    data.setdefault("users", DEFAULT_USERS.copy())
    data.setdefault("tasks", DEFAULT_TASKS.copy())
    data.setdefault("history", [])
    data.setdefault("send_hour", SEND_HOUR)
    data.setdefault("send_minute", SEND_MINUTE)

    seen = set()
    unique_users = []
    for u in data["users"]:
        if u["id"] not in seen:
            seen.add(u["id"])
            unique_users.append(u)
    data["users"] = unique_users

    return data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_users():
    return load_data()["users"]

def get_tasks():
    return load_data()["tasks"]

def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID

def get_today_assignments(day_index: int, users: list, tasks: list):
    if not users:
        return {}
    n = len(users)
    user = users[day_index % n]
    return {str(user["id"]): tasks.copy()}

def make_task_keyboard(user_id: str, tasks: list, completed: list):
    buttons = []
    for task in tasks:
        if task in completed:
            buttons.append([InlineKeyboardButton(
                text=f"✅ {task}",
                callback_data=f"done:{user_id}:{task}"
            )])
        else:
            buttons.append([InlineKeyboardButton(
                text=f"⬜ {task}",
                callback_data=f"done:{user_id}:{task}"
            )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def send_daily_tasks(force: bool = False):
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")

    if not force and data.get("last_send_date") == today:
        return

    users = data["users"]
    tasks = data["tasks"]

    if not users:
        await bot.send_message(ADMIN_ID, "⚠️ Нет пользователей для назначения заданий!")
        return
    if not tasks:
        await bot.send_message(ADMIN_ID, "⚠️ Нет заданий!")
        return

    if data.get("current_assignments") and data.get("last_send_date"):
        data["history"].append({
            "date": data["last_send_date"],
            "assignments": data["current_assignments"],
            "completed": data["completed"]
        })
        data["history"] = data["history"][-30:]

    assignments = get_today_assignments(data["day_index"], users, tasks)
    data["current_assignments"] = assignments
    data["completed"] = {uid: [] for uid in assignments}
    data["last_send_date"] = today
    data["day_index"] += 1
    save_data(data)

    for uid_str, task_list in assignments.items():
        uid = int(uid_str)
        user = next((u for u in users if u["id"] == uid), None)
        name = user["name"] if user else "друг"

        text = (
            f"📅 <b>Задания на сегодня</b>\n\n"
            f"Привет, {name}!\n"
            f"Сегодня твои задания:\n\n"
        )
        for i, t in enumerate(task_list, 1):
            text += f"{i}. {t}\n"
        text += "\nНажми на кнопку, когда выполнишь задание 👇"

        kb = make_task_keyboard(uid_str, task_list, [])

        try:
            await bot.send_message(uid, text, reply_markup=kb, parse_mode=ParseMode.HTML)
        except Exception as e:
            await bot.send_message(
                ADMIN_ID,
                f"⚠️ Не удалось отправить задания {uid}:\n<code>{e}</code>",
                parse_mode=ParseMode.HTML
            )

    summary = "📋 <b>Сегодняшние назначения:</b>\n\n"
    for uid_str, task_list in assignments.items():
        user = next((u for u in users if str(u["id"]) == uid_str), None)
        name = user["username"] if user else uid_str
        summary += f"<b>{name}</b>:\n"
        for t in task_list:
            summary += f"  • {t}\n"
        summary += "\n"
    await bot.send_message(ADMIN_ID, summary, parse_mode=ParseMode.HTML)

# ==================== КОМАНДЫ И КНОПКИ ====================

@dp.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    users = get_users()
    is_user = any(u["id"] == user_id for u in users)

    if is_admin(user_id):
        await message.answer(
            "👋 <b>Админ-панель</b>\n\n"
            "Используй кнопки внизу или команды.\n\n"
            "<b>Основные:</b>\n"
            "/status — статус сегодня\n"
            "/force — отправить задания сейчас\n"
            "/who — кому завтра\n"
            "/history — история\n\n"
            "<b>Пользователи:</b>\n"
            "/users — список\n"
            "/adduser ID Имя @username\n"
            "/deluser ID\n\n"
            "<b>Задания:</b>\n"
            "/tasks — список\n"
            "/addtask Текст\n"
            "/deltask номер\n\n"
            "<b>Другое:</b>\n"
            "/broadcast Текст\n"
            "/reset — сбросить ротацию\n"
            "/settime ЧЧ ММ",
            reply_markup=get_admin_keyboard(),
            parse_mode=ParseMode.HTML
        )
    elif is_user:
        await message.answer(
            "👋 Привет!\n\n"
            "Я присылаю тебе задания каждый день.\n\n"
            "Нажми <b>📋 Мои задания</b> чтобы посмотреть текущие задачи.\n"
            "Когда выполнишь — нажми кнопку ✅ под сообщением.",
            reply_markup=get_user_keyboard(),
            parse_mode=ParseMode.HTML
        )
    else:
        await message.answer("⛔ У тебя нет доступа к этому боту.")

@dp.message(Command("help"))
@dp.message(F.text == "❓ Помощь")
async def cmd_help(message: Message):
    user_id = message.from_user.id

    if is_admin(user_id):
        await cmd_start(message)
        return

    users = get_users()
    if any(u["id"] == user_id for u in users):
        await message.answer(
            "📖 <b>Справка</b>\n\n"
            "📋 Мои задания — посмотреть задания на сегодня\n"
            "❓ Помощь — эта справка\n\n"
            "Бот сам присылает задания каждый день.\n"
            "Чтобы отметить выполнение — нажми кнопку под сообщением.",
            reply_markup=get_user_keyboard(),
            parse_mode=ParseMode.HTML
        )
    else:
        await message.answer("⛔ У тебя нет доступа.")

@dp.message(Command("mytasks"))
@dp.message(F.text == "📋 Мои задания")
async def cmd_mytasks(message: Message):
    user_id = message.from_user.id
    data = load_data()
    users = data["users"]

    if not any(u["id"] == user_id for u in users) and not is_admin(user_id):
        await message.answer("⛔ У тебя нет доступа.")
        return

    uid_str = str(user_id)
    assignments = data.get("current_assignments", {})
    completed = data.get("completed", {})

    if is_admin(user_id) and uid_str not in assignments:
        await message.answer(
            "У тебя нет заданий на сегодня (ты админ).\n"
            "Используй кнопку «📊 Статус»."
        )
        return

    if uid_str not in assignments:
        await message.answer(
            "📭 На сегодня у тебя нет заданий.\n"
            "Бот пришлёт их, когда наступит твоя очередь."
        )
        return

    tasks = assignments[uid_str]
    done = completed.get(uid_str, [])

    text = "📋 <b>Твои задания на сегодня:</b>\n\n"
    for t in tasks:
        mark = "✅" if t in done else "⬜"
        text += f"{mark} {t}\n"

    if len(done) == len(tasks):
        text += "\n🎉 Все задания выполнены!"
    else:
        text += f"\nВыполнено: {len(done)}/{len(tasks)}"

    kb = make_task_keyboard(uid_str, tasks, done)
    await message.answer(text, reply_markup=kb, parse_mode=ParseMode.HTML)

@dp.message(Command("status"))
@dp.message(F.text == "📊 Статус")
async def cmd_status(message: Message):
    if not is_admin(message.from_user.id):
        return

    data = load_data()
    assignments = data.get("current_assignments", {})
    completed = data.get("completed", {})
    users = data["users"]

    if not assignments:
        await message.answer("Сегодня ещё нет назначенных заданий.\nНажми «🚀 Отправить сейчас»")
        return

    text = f"📊 <b>Статус на {data.get('last_send_date', 'сегодня')}:</b>\n\n"
    for uid_str, task_list in assignments.items():
        user = next((u for u in users if str(u["id"]) == uid_str), None)
        name = user["username"] if user else uid_str
        done = completed.get(uid_str, [])
        text += f"<b>{name}</b>\n"
        for t in task_list:
            mark = "✅" if t in done else "⬜"
            text += f"  {mark} {t}\n"
        text += "\n"

    await message.answer(text, parse_mode=ParseMode.HTML)

@dp.message(Command("force"))
@dp.message(F.text == "🚀 Отправить сейчас")
async def cmd_force(message: Message):
    if not is_admin(message.from_user.id):
        return
    await message.answer("⏳ Отправляю задания...")
    await send_daily_tasks(force=True)
    await message.answer("✅ Готово!")

@dp.message(Command("who"))
@dp.message(F.text == "🔮 Кто завтра")
async def cmd_who(message: Message):
    if not is_admin(message.from_user.id):
        return

    data = load_data()
    users = data["users"]
    tasks = data["tasks"]

    if not users:
        await message.answer("Нет пользователей.")
        return

    next_index = data["day_index"] % len(users)
    next_user = users[next_index]

    text = (
        f"🔮 <b>Завтра задания получит:</b>\n\n"
        f"{next_user['username']} ({next_user['name']})\n"
        f"ID: <code>{next_user['id']}</code>\n\n"
        f"<b>Задания:</b>\n"
    )
    for t in tasks:
        text += f"• {t}\n"

    await message.answer(text, parse_mode=ParseMode.HTML)

@dp.message(Command("users"))
@dp.message(F.text == "👥 Пользователи")
async def cmd_users(message: Message):
    if not is_admin(message.from_user.id):
        return

    users = get_users()
    if not users:
        await message.answer("Список пользователей пуст.")
        return

    text = f"👥 <b>Пользователи ({len(users)}):</b>\n\n"
    for i, u in enumerate(users, 1):
        text += f"{i}. {u['username']} — {u['name']}\n   ID: <code>{u['id']}</code>\n\n"
    text += "\nДобавить: /adduser ID Имя @username\nУдалить: /deluser ID"
    await message.answer(text, parse_mode=ParseMode.HTML)

@dp.message(Command("adduser"))
async def cmd_adduser(message: Message, command: CommandObject):
    if not is_admin(message.from_user.id):
        return

    if not command.args:
        await message.answer(
            "Формат:\n<code>/adduser 123456789 Имя @username</code>",
            parse_mode=ParseMode.HTML
        )
        return

    parts = command.args.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("Нужно: ID Имя @username")
        return

    try:
        uid = int(parts[0])
    except ValueError:
        await message.answer("ID должен быть числом.")
        return

    name = parts[1]
    username = parts[2]
    if not username.startswith("@"):
        username = "@" + username

    data = load_data()
    if any(u["id"] == uid for u in data["users"]):
        await message.answer("Этот пользователь уже есть в списке.")
        return

    data["users"].append({"id": uid, "name": name, "username": username})
    save_data(data)
    await message.answer(
        f"✅ Добавлен: {username} ({name}) — <code>{uid}</code>",
        parse_mode=ParseMode.HTML
    )

@dp.message(Command("deluser"))
async def cmd_deluser(message: Message, command: CommandObject):
    if not is_admin(message.from_user.id):
        return

    if not command.args:
        await message.answer(
            "Формат: <code>/deluser 123456789</code>",
            parse_mode=ParseMode.HTML
        )
        return

    try:
        uid = int(command.args.strip())
    except ValueError:
        await message.answer("ID должен быть числом.")
        return

    data = load_data()
    before = len(data["users"])
    data["users"] = [u for u in data["users"] if u["id"] != uid]
    after = len(data["users"])

    if before == after:
        await message.answer("Пользователь не найден.")
    else:
        save_data(data)
        await message.answer(
            f"✅ Пользователь <code>{uid}</code> удалён.",
            parse_mode=ParseMode.HTML
        )

@dp.message(Command("tasks"))
@dp.message(F.text == "📝 Задания")
async def cmd_tasks(message: Message):
    if not is_admin(message.from_user.id):
        return

    tasks = get_tasks()
    if not tasks:
        await message.answer("Список заданий пуст.")
        return

    text = f"📝 <b>Задания ({len(tasks)}):</b>\n\n"
    for i, t in enumerate(tasks, 1):
        text += f"{i}. {t}\n"
    text += "\nДобавить: /addtask Текст\nУдалить: /deltask номер"
    await message.answer(text, parse_mode=ParseMode.HTML)

@dp.message(Command("addtask"))
async def cmd_addtask(message: Message, command: CommandObject):
    if not is_admin(message.from_user.id):
        return

    if not command.args:
        await message.answer(
            "Формат: <code>/addtask 🧹 Помыть пол</code>",
            parse_mode=ParseMode.HTML
        )
        return

    task = command.args.strip()
    data = load_data()
    data["tasks"].append(task)
    save_data(data)
    await message.answer(f"✅ Задание добавлено:\n{task}")

@dp.message(Command("deltask"))
async def cmd_deltask(message: Message, command: CommandObject):
    if not is_admin(message.from_user.id):
        return

    if not command.args:
        await message.answer(
            "Формат: <code>/deltask 2</code> (номер из /tasks)",
            parse_mode=ParseMode.HTML
        )
        return

    try:
        num = int(command.args.strip())
    except ValueError:
        await message.answer("Номер должен быть числом.")
        return

    data = load_data()
    if num < 1 or num > len(data["tasks"]):
        await message.answer(f"Номер должен быть от 1 до {len(data['tasks'])}")
        return

    removed = data["tasks"].pop(num - 1)
    save_data(data)
    await message.answer(f"✅ Удалено:\n{removed}")

@dp.message(Command("history"))
@dp.message(F.text == "📜 История")
async def cmd_history(message: Message):
    if not is_admin(message.from_user.id):
        return

    data = load_data()
    history = data.get("history", [])

    if not history:
        await message.answer("История пока пуста.")
        return

    text = "📜 <b>История (последние 7 дней):</b>\n\n"
    for entry in history[-7:]:
        text += f"<b>{entry['date']}</b>\n"
        for uid_str, task_list in entry.get("assignments", {}).items():
            user = next((u for u in data["users"] if str(u["id"]) == uid_str), None)
            name = user["username"] if user else uid_str
            done = entry.get("completed", {}).get(uid_str, [])
            text += f"  {name}:\n"
            for t in task_list:
                mark = "✅" if t in done else "❌"
                text += f"    {mark} {t}\n"
        text += "\n"

    await message.answer(text, parse_mode=ParseMode.HTML)

@dp.message(Command("reset"))
@dp.message(F.text == "🔄 Сброс")
async def cmd_reset(message: Message):
    if not is_admin(message.from_user.id):
        return

    data = load_data()
    data["day_index"] = 0
    save_data(data)
    await message.answer("✅ Ротация сброшена. Следующий — первый в списке.")

@dp.message(Command("broadcast"))
@dp.message(F.text == "📢 Рассылка")
async def cmd_broadcast(message: Message, command: CommandObject = None):
    if not is_admin(message.from_user.id):
        return

    # Если нажали кнопку — просим текст
    if message.text == "📢 Рассылка":
        await message.answer(
            "Отправь сообщение для рассылки в формате:\n"
            "<code>/broadcast Текст сообщения</code>",
            parse_mode=ParseMode.HTML
        )
        return

    if not command or not command.args:
        await message.answer(
            "Формат: <code>/broadcast Текст сообщения</code>",
            parse_mode=ParseMode.HTML
        )
        return

    text = command.args
    users = get_users()
    ok = 0
    fail = 0

    await message.answer(f"⏳ Рассылка {len(users)} пользователям...")

    for u in users:
        try:
            await bot.send_message(
                u["id"],
                f"📢 <b>Сообщение от админа:</b>\n\n{text}",
                parse_mode=ParseMode.HTML
            )
            ok += 1
        except Exception:
            fail += 1
        await asyncio.sleep(0.05)

    await message.answer(f"✅ Готово: успешно {ok}, ошибок {fail}")

@dp.message(Command("settime"))
@dp.message(F.text == "⏰ Время")
async def cmd_settime(message: Message, command: CommandObject = None):
    if not is_admin(message.from_user.id):
        return

    data = load_data()

    # Если нажали кнопку — показываем текущее время
    if message.text == "⏰ Время":
        await message.answer(
            f"Сейчас время рассылки: <b>{data['send_hour']:02d}:{data['send_minute']:02d}</b>\n\n"
            f"Изменить: <code>/settime 9 0</code>",
            parse_mode=ParseMode.HTML
        )
        return

    if not command or not command.args:
        await message.answer(
            f"Сейчас время: <b>{data['send_hour']:02d}:{data['send_minute']:02d}</b>\n\n"
            f"Формат: <code>/settime 9 0</code>",
            parse_mode=ParseMode.HTML
        )
        return

    parts = command.args.split()
    if len(parts) != 2:
        await message.answer("Нужно два числа: час и минута")
        return

    try:
        hour = int(parts[0])
        minute = int(parts[1])
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError
    except ValueError:
        await message.answer("Час 0–23, минута 0–59")
        return

    data["send_hour"] = hour
    data["send_minute"] = minute
    save_data(data)

    try:
        scheduler.remove_job("daily_tasks")
    except Exception:
        pass

    scheduler.add_job(
        send_daily_tasks,
        trigger="cron",
        hour=hour,
        minute=minute,
        id="daily_tasks"
    )

    await message.answer(
        f"✅ Время рассылки изменено на <b>{hour:02d}:{minute:02d}</b>",
        parse_mode=ParseMode.HTML
    )

# ==================== CALLBACK ====================

@dp.callback_query(F.data.startswith("done:"))
async def on_task_done(callback: CallbackQuery):
    parts = callback.data.split(":", 2)
    if len(parts) < 3:
        await callback.answer("Ошибка данных")
        return

    _, uid_str, task = parts
    user_id = callback.from_user.id

    if str(user_id) != uid_str:
        await callback.answer("Это не твоё задание!", show_alert=True)
        return

    data = load_data()
    completed = data.get("completed", {})
    if uid_str not in completed:
        completed[uid_str] = []

    if task in completed[uid_str]:
        completed[uid_str].remove(task)
        await callback.answer("Отметка снята")
    else:
        completed[uid_str].append(task)
        await callback.answer("Отлично! Задание выполнено 🐦")

        user = next((u for u in data["users"] if u["id"] == user_id), None)
        name = user["username"] if user else str(user_id)
        await bot.send_message(
            ADMIN_ID,
            f"✅ {name} выполнил:\n{task}"
        )

    data["completed"] = completed
    save_data(data)

    tasks = data["current_assignments"].get(uid_str, [])
    kb = make_task_keyboard(uid_str, tasks, completed[uid_str])
    try:
        await callback.message.edit_reply_markup(reply_markup=kb)
    except Exception:
        pass

# ==================== ЗАПУСК ====================

async def main():
    data = load_data()
    hour = data.get("send_hour", SEND_HOUR)
    minute = data.get("send_minute", SEND_MINUTE)

    scheduler.add_job(
        send_daily_tasks,
        trigger="cron",
        hour=hour,
        minute=minute,
        id="daily_tasks"
    )
    scheduler.start()

    print(f"Бот запущен. Рассылка в {hour:02d}:{minute:02d}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())