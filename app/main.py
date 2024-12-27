
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import logging
import sys
import os

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
    host_name = os.getenv("HOSTNAME", "unknown")
    rtn_val = f"ping-pong is running from pod: {host_name}"
    logger.info(f"/ was accessed on {host_name}")
    return templates.TemplateResponse("index.html", {"request": request, "message": rtn_val})


@app.get("/ping")
def health():
    logger.info("/ping - got pinged")
    return {"ping": "got pinged... "}


@app.get("/pong")
def health():
    logger.info("/pong - got ponged")
    return {"ping": "got pinged... "}


@app.get("/health")
def health():
    logger.info("/health - ping-pong is healthy")
    return {"message": "Ping-Pong is Healthy"}

