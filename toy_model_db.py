import sqlite3


conn = sqlite3.connect(":memory:")
cursor = conn.cursor()


def initialize_db():
    cursor.execute("drop table if exists position")
    cursor.execute("create table position (x int, y int, face string)")


def set_placement(x: int, y: int, face: str):
    remove_toy_model_instance()
    cursor.execute(f"insert into position values ({x}, {y}, '{face}')")


def get_placement():
    return cursor.execute("select * from position").fetchone()


def get_coordinates():
    return cursor.execute("select x, y from position").fetchone()


def get_direction():
    return cursor.execute("select face from position").fetchone()


def update_position(x: int, y: int):
    cursor.execute(f"update position set x={x}, y={y}")


def update_direction(face: str):
    cursor.execute(f"update position set face='{face}'")


def remove_toy_model_instance():
    cursor.execute("delete from position")


def close_connection():
    conn.commit()
    conn.close()
