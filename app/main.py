
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),  # Log to stdout for cloud-native compatibility
    ],
)

logger = logging.getLogger("ping-pong")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    logger.info("/ was accessed.")
    return templates.TemplateResponse(request, "index.html", {"message": "The app is up and running!"})

@app.get("/health")
def health():
    logger.info("/health - ping-pong is healthy")
    return {"message": "Ping-Pong is Healthy"}

