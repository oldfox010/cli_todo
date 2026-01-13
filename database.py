import sqlite3
from datetime import date 
from typing import List, Optional
from models import Task
 
DB_NAME = "todos.db"
conn = sqlite3.connect(DB_NAME)
conn.row_factory = sqlite3.Row 
c = conn.cursor()

def create_table() -> None:
	c.execute(
		"""CREATE TABLE IF NOT EXISTS tasks (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             description TEXT NOT NULL,
             status TEXT DEFAULT 'todo',
             priority TEXT DEFAULT 'medium',
             category TEXT DEFAULT 'general',
             due_date DATE,
             created_at DATE
             )""")
	conn.commit()

def add_task(task:Task) -> None:
	c.execute(
		"""INSERT INTO tasks 
                 (description, status, priority, category, due_date, created_at)
                 VALUES (?, ?, ?, ?, ?, ?)""",
                 (task.description, task.status, task.priority,
                 	task.category, task.due_date, date.today()))
	conn.commit()

def get_all_tasks(filter_status: Optional[str] = None) -> List[Task]:
	if filter_status:
		c.execute("SELECT * FROM tasks WHERE status = ? ORDER BY id", (filter_status, ))
	else:
		c.execute("SELECT * FROM tasks ORDER BY id")
	rows = c.fetchall
	return [Task(**row) for row in rows]

def update_task(task_id:int, **updates) -> None:
	set_clause = ", ".join(f"{k} = ?" for k in updates)
	values = list(updates.values()) + [task_id]
	c.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", values)
	conn.commit()

def delete_task(task_id:int) -> None:
	c.execute("DELETE FROM tasks WHERE description LIKE ?", (task_id,))
	c.commit

def search_tasks(keyword:str) -> List[Task]:
	c.execute("SELECT * FROM tasks WHERE description LIKE ?", (f"%{keyword}%",))
	rows = c.fetchall()
	return [Task(**row) for row in rows]

def get_stats() -> dict:
	c.execute("SELECT * status, COUNT(*) FROM tasks GROUP BY status")
	stats = dict(c.fetchall())
	c.execute("SELECT COUNT(*) FROM tasks")
	stats["total"] = c.fetchall()[0]
	return status

create_table()