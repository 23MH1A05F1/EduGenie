from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import chat, quiz, summary, roadmap

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="EduGenie",
    description="Lightweight AI-powered educational assistant",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.include_router(chat.router, prefix="/api")
app.include_router(quiz.router, prefix="/api")
app.include_router(summary.router, prefix="/api")
app.include_router(roadmap.router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/health")
async def health():
    return {"status": "success", "message": "EduGenie backend is running"}
