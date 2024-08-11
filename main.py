from fastapi import FastAPI, HTTPException
import os
import sys
import uvicorn
from typing import List, Callable
from functools import wraps

if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.dirname(__file__))

import toy_model_db
from interfaces import Coordinate, FACES


app = FastAPI()
toy_model_db.initialize_db()


def check_toy_model(request_view: Callable):
    @wraps(request_view)
    async def wrapper(*args, **kwargs):
        if not toy_model_db.get_placement():
            error_message = "Toy model not placed yet."
            raise HTTPException(status_code=400, detail=error_message)

        return await request_view(*args, **kwargs)

    return wrapper


def get_direction_index():
    direction = toy_model_db.get_direction()
    return FACES.index(direction[0])


def handle_direction(rotation: int):
    new_index = (get_direction_index() + rotation) % 4
    toy_model_db.update_direction(FACES[new_index])


def handle_movement(coordinates: List[int]):
    checked_values = list(filter(lambda coor: 0 <= coor <= 5, coordinates))
    if checked_values == coordinates:
        toy_model_db.update_position(coordinates[0], coordinates[1])
        return True

    return False


@app.get("/")
async def root():
    return {"message": "Qarbon Assessment"}


@app.post("/place")
async def place(coord: Coordinate):
    toy_model_db.set_placement(coord.x, coord.y, coord.face.value)
    return {"message": "Toy model placed."}


@app.post("/move")
@check_toy_model
async def move():
    coordinates = list(toy_model_db.get_coordinates())
    index = get_direction_index()
    if index % 2:
        coordinates[0] += 1 if FACES[index] == "EAST" else -1
    else:
        coordinates[1] += 1 if FACES[index] == "NORTH" else -1

    if handle_movement(coordinates):
        return {"message": "Toy model moved one unit forward."}

    return {"message": "Toy model did not move."}


@app.post("/left")
@check_toy_model
async def left():
    handle_direction(-1)
    return {"message": "Toy model rotated 90deg to the left."}


@app.post("/right")
@check_toy_model
async def right():
    handle_direction(1)
    return {"message": "Toy model rotated 90deg to the right."}


@app.get("/report")
@check_toy_model
async def report():
    toy_model = toy_model_db.get_placement()
    face = toy_model[2]
    coordinates = (toy_model[0], toy_model[1])
    return {"message": f"Toy model placed at {coordinates} facing {face}."}


@app.delete("/remove")
async def remove():
    toy_model_db.remove_toy_model_instance()
    return {"message": "Toy model instance removed."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    toy_model_db.close_connection()
