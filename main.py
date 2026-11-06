
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="My Cloud Phone API")

# Cho phép frontend GitHub Pages gọi backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hoan04254-lab.github.io"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

# 20 thiết bị demo
devices: Dict[int, dict] = {
    i: {
        "id": i,
        "name": f"Android {i}",
        "status": "stopped"
    }
    for i in range(1, 21)
}


class DeviceCommand(BaseModel):
    command: str


@app.get("/")
def home():
    return {
        "message": "My Cloud Phone Backend",
        "status": "online"
    }


@app.get("/api/devices")
def get_devices():
    return list(devices.values())


@app.get("/api/devices/{device_id}")
def get_device(device_id: int):
    if device_id not in devices:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    return devices[device_id]


@app.post("/api/devices/{device_id}/start")
def start_device(device_id: int):
    if device_id not in devices:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    devices[device_id]["status"] = "running"

    return {
        "success": True,
        "device": devices[device_id]
    }


@app.post("/api/devices/{device_id}/stop")
def stop_device(device_id: int):
    if device_id not in devices:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    devices[device_id]["status"] = "stopped"

    return {
        "success": True,
        "device": devices[device_id]
    }


@app.post("/api/devices/{device_id}/command")
def send_command(
    device_id: int,
    data: DeviceCommand
):
    if device_id not in devices:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    return {
        "success": True,
        "device_id": device_id,
        "command": data.command,
        "message": "Command received"
    }
