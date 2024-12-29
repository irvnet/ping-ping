
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import logging
import sys
import os
import httpx

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
def ping():
    logger.info("/ping - got pinged")
    return {"ping": "got pinged... "}


@app.get("/pong")
def pong():
    logger.info("/pong - got ponged")
    return {"pong": "got ponged... "}

@app.get("/dpong")
def discover_and_pong():
    pong_service_url = "http://pong-svc.default.svc.cluster.local:8000/ping"
    try:
        logger.info(f"hitting /ping on pong-deployment @ {pong_service_url}")
        with httpx.Client() as client:
            response = client.get(pong_service_url)
        logger.info(f"pong response: {response.json()}")
        return {"message": "/ping sent to pong-deployment", "pong_response": response.json()}
    except httpx.RequestError as e:
        logger.error(f"Failed to contact pong: {e}")
        return {"error": "Failed to contact pong", "details": str(e)}


@app.get("/dynamic-pongs")
def discover_and_ping_all():
    from kubernetes import client, config
    try:
        # Load Kubernetes configuration (works in-cluster)
        config.load_incluster_config()
        v1 = client.CoreV1Api()

        # Find all pods with the label app=ping-pong and identity=pong
        pods = v1.list_namespaced_pod(
            namespace="default", label_selector="app=pong"
        )

        results = []
        with httpx.Client() as client:
            for pod in pods.items:
                pod_ip = pod.status.pod_ip
                if pod_ip:
                    pong_url = f"http://{pod_ip}:8000/pong"
                    try:
                        response = client.get(pong_url)
                        logger.info(f"ponged pod at {pod_ip}, Response: {response.json()}")
                        results.append({"pod_ip": pod_ip, "says: ": response.json()})
                    except httpx.RequestError as e:
                        logger.error(f"Failed to ping pong at {pod_ip}: {e}")
                        results.append({"pod_ip": pod_ip, "error": str(e)})
        return {"message": "Pinged all pongs", "results": results}

    except Exception as e:
        logger.error(f"Error discovering and pinging pongs: {e}")
        return {"error": "Failed to discover pongs", "details": str(e)}


@app.get("/healthz")
def healthz():
    logger.info("/healthz - ping-pong is healthy")
    return {"message": "Ping-Pong is Healthy"}

