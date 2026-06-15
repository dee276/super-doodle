from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class ColumnModel(Base):
    __tablename__ = "columns"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    position = Column(Integer, default=0) # Pour gérer l'ordre des colonnes de gauche à droite

    # Relation : Une colonne peut avoir plusieurs tâches
    tasks = relationship("TaskModel", back_populates="column", cascade="all, delete-orphan")


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    position = Column(Integer, default=0) # Pour gérer l'ordre des tâches de haut en bas
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Clé étrangère pour lier la tâche à une colonne
    column_id = Column(Integer, ForeignKey("columns.id", ondelete="CASCADE"), nullable=False)

    # Relation inverse pour accéder facilement à la colonne depuis la tâche
    column = relationship("ColumnModel", back_populates="tasks")