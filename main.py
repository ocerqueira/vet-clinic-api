from fastapi import FastAPI
from app.config.database import init_db
from app.routes import users, clients, patients, auth


app = FastAPI(title="Clinica Veterinária API", version="1.0")

init_db()

app.include_router(users.router, prefix="/api")
app.include_router(clients.router, prefix="/api")
app.include_router(patients.router, prefix="/api")
app.include_router(auth.router, prefix="/auth")

@app.get("/")
async def root():
    return {"message":"Bem-vindo à API da Clínica Veterinária"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)