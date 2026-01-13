import typer
from datetime import date 
from typing import Optional

from rich.console import Console
from rich.table import Table
from rich import box

from database import (add_task, get_all_tasks, update_task, delete_task, search_tasks, get_stats)
from models import Task

app = typer.Typer(help = "Dope Todo CLI App")
console = Console()

def show_tasks(tasks):
	table = Table(title="Your Tasks", box=box.ROUNDED)
	table.add_column("ID", style="cyan", justify="right")
	table.add_column("Status", justify="center")
	table.add_column("Description", style="bold")
	table.add_column("Priority", justify="center")
	table.add_column("Category")
	table.add_column("Due Date", style="magenta")

	for task in tasks:
		status_color = {"todo": "yellow", "in-progress": "blue", "done": "green"}.get(task.status, "white")
		priority_color = { "low": "green", "medium": "yellow", "high": "red"}.get(task.priority, "white")
		due = task.due_date or "-"
		if task.due_date and task.due_date < date.today():
			due = f"[red]{due} (overdue)[/red]"

		table.add_row(

			str(task.id),
			f"[{status_color}]{task.status}[/{status_color}]",
			task.description,
			f"[{priority_color}]{task.priority}[/{priority_color}]",
			task.category,
			due
		)
	console.print(table)

@app.command()
def add(
	description:str = typer.Argument(..., help="Task description"),
	priority: str = typer.Option("medium", "--priority", help = "low/medium/high"),
	category:str = typer.Option("general", "--category"),
	due: Optional[str] = typer.Option(None, "--due", help = "Due date YYYY-MM-DD")
):
	"""add new task"""
	due_date = date.fromisoformat(due) if due else None
	task = Task(description = description, priority = priority,
				category = category, due_date = due_date)
	add_task(task)
	console.print("[green] Task added ✅ ![/green]")
	show_tasks(get_all_tasks())

@app.command()
def list(status:Optional[str]=typer.Option(None, "--status", help = "filter: todo/in-progress/done")):
	"""list all tasks or filtered by status"""
	tasks = get_all_tasks(filter_status = status)
	show_tasks(tasks)


@app.command
def update(
	task_id:int,
	description: Optional[str] = None,
	priority: Optional[str] = None,
	category: Optional[str] = None,
	due: Optional[str] = None
):

	"""update a task"""
	updates = {}
	if description: updates["description"] = description
	if priority: updates["priority"] = priority
	if category: updates["category"] = category
	if due: updates["due_date"] = date.fromisoformat(due)
	update_task(task_id, **updates)
	console.print("[green] task updated✅! [/green]")
	show_tasks(get_all_tasks())

@app.command
def mark(
	task_id: int,
	status: str = typer.Argument(..., help = "todo/in-progress/done")
):
	""" mark task status """
	update_task(task_id, status=status)
	console.print(f"[green] Marked as {status} [/green]")
	show_tasks(get_all_tasks())

@app.command
def delete(task_id:int):
	"""delete a task"""
	delete_task(task_id)
	console.print(f"[red] task deleted:{task} [/red]")
	show_tasks(get_all_tasks())

@app.command
def search(keyword:str):
	"""search tasks by keyword"""
	task = search_tasks(keyword)
	show_tasks(task)

@app.command
def stats():
	"""show task statistics"""
	s = get_stats()
	console.print(f"[bold] Total:[/bold] {s.get('total', 0)}")
	console.print(f"[yellow]Todo:[/yellow] {s.get('todo', 0)}")
	console.print(f"[blue]In-progress:[/blue] {s.get('in-progress', 0)}")
	console.print(f"[green]Done:[/green] {s.get('done', 0)}")

if __name__ == "__main__":
	app()	