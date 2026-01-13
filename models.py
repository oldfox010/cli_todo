from dataclasses import dataclass
from datetime import date 
from typing import Optional 

@dataclass
class Task:
	id: Optional[int] = None
	description: str = ""
	status: str = "todo"  # todo, in-progress, done
	priority: str = "medium"  # low, medium, high
	category: str = "general"
	due_date: Optional[date] = None
	created_at: Optional[date] = None