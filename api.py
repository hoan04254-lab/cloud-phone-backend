
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
    devices[device_id]["status"] = "running"
    return devices[device_id]

@app.post("/api/devices/{device_id}/stop")
def stop_device(device_id: int):
    if device_id not in devices:
        raise HTTPException(404, "Device not found")
    devices[device_id]["status"] = "stopped"
    return devices[device_id]
