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

@app.delete("/api/cars/{id}", status_code = 204)
def remove_car(id: int) -> None:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        db.remove(car)
        save_db(db)
    else:
        raise HTTPException(status_code = 404, detail=f'No car with id={id}')

@app.put("/api/cars/{id}", response_model = CarOutput)
def change(id: int, new_data: CarInput) -> CarOutput:
      matches = [car for car in db if car.id == id]
      if matches:
          car = matches[0]
          car.fuel = new_data.fuel
          car.transmission = new_data.transmission
          car.size = new_data.size
          car.doors = new_data.doors
          save_db(db)
          return car
      else:
          raise HTTPException(status_code = 404, detail =f"No car with id={id}" )

if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)

     