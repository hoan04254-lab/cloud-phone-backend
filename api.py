
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Cloud Phone API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hoan04254-lab.github.io"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

devices = {
    i: {
        "id": i,
        "name": f"Android {i}",
        "status": "stopped"
    }
    for i in range(1, 21)
}

@app.get("/")
def home():
    return {"message": "Cloud Phone API", "status": "online"}

@app.get("/api/devices")
def list_devices():
    return list(devices.values())

@app.post("/api/devices/{device_id}/start")
def start_device(device_id: int):
    if device_id not in devices:
        raise HTTPException(404, "Device not found")

    result = send_android_command(device_id, "start")

    devices[device_id]["status"] = "running"
    devices[device_id]["android_result"] = result

    return devices[device_id]

@app.post("/api/devices/{device_id}/stop")
def stop_device(device_id: int):
    if device_id not in devices:
        raise HTTPException(404, "Device not found")

    result = send_android_command(device_id, "stop")

    devices[device_id]["status"] = "stopped"
    devices[device_id]["android_result"] = result

    return devices[device_id]:import os
import requests

ANDROID_HOST = os.getenv("ANDROID_HOST", "").rstrip("/")
ANDROID_HOST_TOKEN = os.getenv("ANDROID_HOST_TOKEN", "")


def send_android_command(device_id: int, action: str):
    if not ANDROID_HOST:
        raise HTTPException(
            status_code=503,
            detail="Android host chưa được kết nối"
        )

    try:
        response = requests.post(
            f"{ANDROID_HOST}/devices/{device_id}/{action}",
            headers={
                "Authorization": f"Bearer {ANDROID_HOST_TOKEN}"
            },
            timeout=15
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Không gửi được lệnh tới máy chủ Android"
        ) int):
    if device_id not in devices:
        raise HTTPException(404, "Device not found")
    devices[device_id]["status"] = "stopped"
    return devices[device_id]
