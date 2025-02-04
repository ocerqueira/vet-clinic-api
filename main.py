from fastapi import FastAPI

app = FastAPI(title="Clinica Veterinária API", version="1.0")

@app.get("/")
async def root():
    return {"message":"Bem-vindo à API da Clínica Veterinária"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)