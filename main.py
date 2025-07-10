from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Estudiante

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear Estudiante
@app.post("/estudiantes/")
def crear_estudiante(estudiante: dict, db: Session = Depends(get_db)):
    nuevo = Estudiante(**estudiante)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

# Listar todos los estudiantes
@app.get("/estudiantes/")
def listar_estudiantes(db: Session = Depends(get_db)):
    return db.query(Estudiante).all()

# Listar por ID
@app.get("/estudiantes/{id}")
def listar_por_id(id: int, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).get(id)
    if not estudiante:
        raise HTTPException(status_code=404, detail="No encontrado")
    return estudiante

# Estudiantes con promedio mayor a  30
@app.get("/estudiantes/promedio30/")
def promedio_30(db: Session = Depends(get_db)):
    return db.query(Estudiante).filter(Estudiante.promedio > 30).all()

# Actualizar Estudiante
@app.put("/estudiantes/{id}")
def actualizar_estudiante(id: int, datos: dict, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).get(id)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    for key, value in datos.items():
        setattr(estudiante, key, value)
    db.commit()
    return estudiante

# Eliminar Estudiante
@app.delete("/estudiantes/{id}")
def eliminar_estudiante(id: int, db: Session = Depends(get_db)):
    estudiante = db.query(Estudiante).get(id)
    if not estudiante:
        raise HTTPException(status_code=404, detail="No encontrado")
    db.delete(estudiante)
    db.commit()
    return {"ok": True}
