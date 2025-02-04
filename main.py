from fastapi import FastAPI
from app.config.database import init_db
from app.routes import users

init_db()

app = FastAPI(title="Clinica Veterinária API", version="1.0")

@app.get("/")
async def root():
    return {"message":"Bem-vindo à API da Clínica Veterinária"}

app.include_router(users.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)