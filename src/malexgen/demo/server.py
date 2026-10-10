from pathlib import Path

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from ..utils.logger import logger


SITE_DIR = Path(__file__).parent / "site"


app = FastAPI(
    title="MalExtGenerator Demo",
    description="Демо-сайт для безопасного тестирования расширений",
    version="1.0.0",
)


if SITE_DIR.exists():
    app.mount("/static", StaticFiles(directory=SITE_DIR), name="static")


def render(filename: str) -> HTMLResponse:
    path = SITE_DIR / filename
    if not path.exists():
        return HTMLResponse(
            f"<h1>404</h1><p>Файл не найден: {filename}</p>",
            status_code=404,
        )
    return HTMLResponse(path.read_text(encoding="utf-8"))


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    return render("index.html")


@app.get("/login", response_class=HTMLResponse)
async def login_page() -> HTMLResponse:
    return render("login.html")


@app.get("/crypto", response_class=HTMLResponse)
async def crypto_page() -> HTMLResponse:
    return render("crypto.html")


@app.get("/payment", response_class=HTMLResponse)
async def payment_page() -> HTMLResponse:
    return render("payment.html")


@app.get("/chat", response_class=HTMLResponse)
async def chat_page() -> HTMLResponse:
    return render("chat.html")

@app.post("/api/login")
async def api_login(request: Request) -> JSONResponse:

    try:
        data = await request.json()
    except Exception:
        data = {}

    username = data.get("username", "")
    password = data.get("password", "")

    logger.info(
        f"[DEMO] Login attempt: username='{username[:3]}***' "
        f"password_length={len(password)}"
    )

    return JSONResponse({
        "status": "ok",
        "message": "Демо: данные перехвачены (см. консоль расширения)",
        "demo": True,
    })


@app.post("/api/payment")
async def api_payment(request: Request) -> JSONResponse:
    try:
        data = await request.json()
    except Exception:
        data = {}

    logger.info(f"[DEMO] Payment attempt: fields={list(data.keys())}")

    return JSONResponse({
        "status": "ok",
        "message": "Демо: данные перехвачены",
        "demo": True,
    })


@app.post("/api/chat")
async def api_chat(request: Request) -> JSONResponse:
    try:
        data = await request.json()
    except Exception:
        data = {}

    message = data.get("message", "")
    logger.info(f"[DEMO] Chat message: {len(message)} chars")

    return JSONResponse({
        "status": "ok",
        "reply": "Демо-ответ: сообщение получено",
        "demo": True,
    })


@app.get("/api/cookies")
async def api_cookies(request: Request) -> JSONResponse:
    cookies = dict(request.cookies)
    masked = {
        k: (v[:10] + "..." if len(v) > 10 else v)
        for k, v in cookies.items()
    }
    return JSONResponse({"cookies": masked})


@app.get("/api/headers")
async def api_headers(request: Request) -> JSONResponse:
    return JSONResponse({
        "headers": dict(request.headers),
        "client": request.client.host if request.client else None,
    })


@app.get("/api/health")
async def api_health() -> JSONResponse:
    return JSONResponse({
        "status": "ok",
        "service": "MalExtGenerator Demo",
        "version": "1.0.0",
    })


@app.get("/api/set-demo-cookies")
async def set_demo_cookies() -> JSONResponse:
    response = JSONResponse({
        "status": "ok",
        "message": "Демо-куки установлены",
        "cookies_set": [
            "session_id",
            "auth_token",
            "user_prefs",
        ],
    })
    response.set_cookie("session_id", "demo_session_abc123xyz", httponly=False)
    response.set_cookie("auth_token", "demo_jwt_token_eyJhbGciOi...", httponly=False)
    response.set_cookie("user_prefs", "theme=dark&lang=ru", httponly=False)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


__all__ = ["app"]
