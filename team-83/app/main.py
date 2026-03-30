from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api import subscribers, devices

app = FastAPI(title="webOS Subscription Service")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(subscribers.router, prefix="/api", tags=["Subscribers"])
app.include_router(devices.router, prefix="/api", tags=["Devices"])


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(
    request=request, 
    name="index.html", 
    context={"request": request}
)


@app.get("/health")
def health():
    return {"status": "ok"}
