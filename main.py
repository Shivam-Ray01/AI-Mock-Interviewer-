from fastapi import FastAPI
from database import Base, engine
import models

app = FastAPI(title="AI Mock Interviewer")

Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    print("Terminal is working properly...")
    return {"status": "ok"}
