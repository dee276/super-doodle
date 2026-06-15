from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- SCHÉMAS POUR LES TÂCHES ---
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    position: int = 0

class TaskCreate(TaskBase):
    column_id: int  # Requis pour créer une tâche

class Task(TaskBase):
    id: int
    column_id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Permet à Pydantic de lire les modèles SQLAlchemy


# --- SCHÉMAS POUR LES COLONNES ---
class ColumnBase(BaseModel):
    title: str
    position: int = 0

class ColumnCreate(ColumnBase):
    pass

class Column(ColumnBase):
    id: int
    tasks: List[Task] = []  # Une colonne inclura la liste de ses tâches !

    class Config:
        from_attributes = True