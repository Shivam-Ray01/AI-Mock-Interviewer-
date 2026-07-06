from fastapi import FastAPI

app = FastAPI(title="AI Mock Interviewer")

@app.get("/")
def health_check():
    print("Terminal is working properly...")
    return {"status": "ok"}

health_check()