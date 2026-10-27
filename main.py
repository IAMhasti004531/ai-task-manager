from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel

app = FastAPI()

# راه‌اندازی دیتابیس
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class Task(BaseModel):
    title: str

# تابع هوش مصنوعی ساده برای تشخیص دسته‌بندی بر اساس کلمات کلیدی متن
def ai_categorize(title: str) -> str:
    title_lower = title.lower()
    if any(word in title_lower for word in ["خرید", "فروش", "پول", "بانک", "شیر", "نان"]):
        return "🛒 خرید و مالی"
    elif any(word in title_lower for word in ["کد", "برنامه", "باگ", "توسعه", "پروژه", "api"]):
        return "💻 برنامه‌نویسی و کار"
    elif any(word in title_lower for word in ["ورزش", "باشگاه", "دکتر", "سلامت", "خواب"]):
        return "🏋️ سلامت و ورزش"
    else:
        return "📌 عمومـی"

# گرفتن لیست تسک‌ها
@app.get("/tasks")
def get_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, category FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1], "category": r[2]} for r in rows]

# اضافه کردن تسک با دسته‌بندی هوشمند
@app.post("/tasks")
def add_task(task: Task):
    # اینجا هوش مصنوعی متن را تحلیل می‌کند و دسته را تعیین می‌کند
    detected_category = ai_categorize(task.title)
    
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, category) VALUES (?, ?)", (task.title, detected_category))
    conn.commit()
    conn.close()
    return {
        "message": "تسک با موفقیت و به صورت هوشمند اضافه شد!",
        "title": task.title,
        "assigned_category": detected_category
    }