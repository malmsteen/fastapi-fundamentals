from fastapi import FastAPI, HTTPException
import uvicorn
from schemas import load_db, CarInput, CarOutput, save_db
from datetime import datetime


app = FastAPI()

db = load_db()

@app.get("/")
def welcome(name):
    """Welcome message"""
    return {'message': f"Welcome, {name},  to the car sharing service!"}


@app.get("/date")
def date():
    return {'date': datetime.now()}

@app.get("/api/cars")
def cars(size: str|None = None, doors: int|None = None) -> list:
    result = db
    if size:
        result = [car for car in result if car.size == size]
    if doors:
        result = [car for car in result if car.doors >= doors]
    return result

@app.get("/api/cars/{id}")
def car_by_id(id: int)->CarOutput:
    result = [car for car in db if car.id == id]
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail=f"No car found with id={id}")

@app.post("/api/cars")
def add_car(car: CarInput) -> CarOutput:
    new_car = CarOutput(size=car.size, doors=car.doors,
                        fuel=car.fuel, transmission=car.transmission,
                        id =len(db) + 1)
    db.append(new_car)
    save_db(db)
    return new_car

if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)

     