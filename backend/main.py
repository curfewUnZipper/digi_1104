from fastapi import FastAPI
import multiprocessing
import math
import time
import threading

app = FastAPI()

EC_PATH = "/sys/kernel/debug/ec/ec0/io"

workers = []
target_stage = 7


def read_ec():
    with open(EC_PATH, "rb") as f:
        return list(f.read())


def stress():
    x = 0
    while True:
        x += math.sqrt(12345)


def add_worker():
    p = multiprocessing.Process(target=stress)
    p.start()
    workers.append(p)


def remove_worker():
    if workers:
        p = workers.pop()
        p.terminate()


# ===== CONTROL LOOP (runs forever) =====
def controller_loop():
    global target_stage
    while True:
        data = read_ec()
        stage = data[85]

        if stage < target_stage - 1:
            add_worker()
        elif stage > target_stage + 1:
            remove_worker()

        time.sleep(2)


threading.Thread(target=controller_loop, daemon=True).start()


# ===== API =====

@app.get("/status")
def get_status():
    data = read_ec()
    return {
        "stage": data[85],
        "fan1": data[86],
        "fan2": data[88],
        "workers": len(workers),
        "target": target_stage
    }


@app.post("/set/{stage}")
def set_stage(stage: int):
    global target_stage
    target_stage = stage
    return {"message": f"Target stage set to {stage}"}