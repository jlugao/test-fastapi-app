from app_factory import app_factory

app = app_factory()


@app.get("/ping", status_code=200)
async def ping():
    return {"message": "pong"}
