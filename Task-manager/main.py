from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import engine, get_db

# Créer les tables si elles n'existent pas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Trello Clone API")


# ==========================================
# ROUTES POUR LES COLONNES (COLUMNS)
# ==========================================

# 1. Récupérer toutes les colonnes (avec leurs tâches incluses)
@app.get("/columns", response_model=List[schemas.Column])
def get_columns(db: Session = Depends(get_db)):
    # On trie par le champ 'position' pour que le tableau s'affiche dans le bon ordre
    return db.query(models.ColumnModel).order_by(models.ColumnModel.position).all()

# 2. Créer une nouvelle colonne
@app.post("/columns", response_model=schemas.Column, status_code=status.HTTP_201_CREATED)
def create_column(column: schemas.ColumnCreate, db: Session = Depends(get_db)):
    db_column = models.ColumnModel(**column.model_dump())
    db.add(db_column)
    db.commit()
    db.refresh(db_column)
    return db_column

# 3. Supprimer une colonne
@app.delete("/columns/{column_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_column(column_id: int, db: Session = Depends(get_db)):
    db_column = db.query(models.ColumnModel).filter(models.ColumnModel.id == column_id).first()
    if not db_column:
        raise HTTPException(status_code=404, detail="Colonne introuvable")
    db.delete(db_column)
    db.commit()
    return


# ==========================================
# ROUTES POUR LES TÂCHES (TASKS)
# ==========================================

# 1. Créer une tâche dans une colonne spécifique
@app.post("/tasks", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    # On vérifie d'abord si la colonne existe bel et bien
    db_column = db.query(models.ColumnModel).filter(models.ColumnModel.id == task.column_id).first()
    if not db_column:
        raise HTTPException(status_code=404, detail="La colonne spécifiée n'existe pas")
        
    db_task = models.TaskModel(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# 2. Supprimer une tâche
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.TaskModel).filter(models.TaskModel.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    db.delete(db_task)
    db.commit()
    return