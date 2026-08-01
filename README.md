# Radiator Springs Garage Management System

A menu-driven Python console application for managing a garage of Racer and Support Vehicle cars, built to demonstrate core Object-Oriented Programming concepts: **Inheritance**, **Polymorphism**, and **Encapsulation**.

## Features

- **Check In** a car (Racer or Support Vehicle) with full input validation
- **View Garage** — list every car currently checked in
- **Tune-Up** — find a car by number and edit its fields
- **Retire** — remove a car, with a confirmation prompt
- **Search** — find a car by name or number
- **Garage Report** — total cars, average performance score, breakdown per racing team
- **Persistence** — all data is saved to `garage_data.json` after every change, and reloaded automatically on startup

## OOP Design

```
Car (base class)
 ├── Racer_car        (adds: races_completed, laps_completed)
 └── Support_Vehicle  (adds: crew_size, reliability_rating)

Garage
 └── holds a list of Car objects (composition, not inheritance)
```

- **Inheritance:** `Racer_car` and `Support_Vehicle` both extend `Car`, reusing shared fields (number, name, age, team, speed, capacity) via `super().__init__()`.
- **Polymorphism:** `preformance_score()` and `display_info()` are defined differently in each subclass. Calling either method on a mixed list of cars automatically runs the correct version depending on the object's actual type — no `if/elif` type-checking needed by the caller.
- **Encapsulation:** every attribute is private (`self._x`) and only reachable through `@property` / `@x.setter` pairs, with validation happening *inside* the setter (e.g. rejecting non-positive speed/age), not scattered through the menu code.

## Bugs I Ran Into (and How I Fixed Them)

This is a log of real mistakes made while building this project, kept here so I remember *why* the code looks the way it does — and in case they're useful to anyone else hitting the same errors.

### 1. `__intit__` typo
```python
def __intit__(self, ...):   # wrong — never gets called as a constructor
```
**Fix:** it has to be exactly `__init__`, or Python won't recognize it as the constructor at all.

### 2. No encapsulation — attributes were fully public
```python
self.speed = speed   # anyone can later do car.speed = -999, nothing stops them
```
**Fix:** wrap each attribute in a `@property` getter and a `@x.setter` that validates before storing:
```python
@property
def speed(self):
    return self._speed

@speed.setter
def speed(self, value):
    if value <= 0:
        raise ValueError("Speed must be positive.")
    self._speed = value
```

### 3. Setter function named wrong
```python
@age.setter
def speed(self, value):   # decorator says age, function name says speed — this silently overwrites the real speed setter!
```
**Fix:** the function name after `@x.setter` must match the property name exactly:
```python
@age.setter
def age(self, value):
    ...
```

### 4. Default argument before a non-default argument
```python
def __init__(self, number, name="none", age, type, RacingTeam="none", speed, capacity):
```
**Error:** `SyntaxError: parameter without a default follows parameter with a default`
**Fix:** either give every parameter after the first default a default too, or (simpler) remove the defaults entirely and require all fields to be passed in.

### 5. Method name casing mismatch broke polymorphism
```python
class Racer_car(Car):
    def Preformance_score(self): ...   # capital P

class Support_Vehicle(Car):
    def preformance_score(self): ...   # lowercase p
```
**Problem:** looping through a mixed list and calling `.preformance_score()` on each car would crash on whichever type didn't match that exact casing.
**Fix:** both subclasses must use the **exact same method name** so it can be called uniformly regardless of the object's type.

### 6. Broken "already exists" check using `range(len())`
```python
def check_in_car(self, car):
    for i in range(len(self.cars)):
        if i in self.cars:              # comparing an index number to Car OBJECTS — never true
            raise ValueError("exists")
        else:
            self.cars.append(car)       # appending inside the loop = duplicates, and never runs on an empty list
```
**Fix:** loop through the actual car objects, compare `.number` to `.number`, and append once, *after* the loop confirms no match:
```python
def check_in_car(self, car):
    for existing_car in self.cars:
        if existing_car.number == car.number:
            raise ValueError("this car number already exists.")
    self.cars.append(car)
```

### 7. `from car import ...` when everything was in one file
```python
from car import Car, Racer_car, Support_Vehicle   # ModuleNotFoundError — there is no car.py file
```
**Fix:** if all classes live in a single `.py` file, no import is needed at all — just make sure `Garage` is defined *after* `Car`/`Racer_car`/`Support_Vehicle` in the file so it can see them.

### 8. `view_garage` printed raw objects instead of readable info
```python
def view_grage(self):
    return f'the cars in the grage are {self.cars}'   # prints <__main__.Car object at 0x...>
```
**Fix:** loop through and call the `display_info()` method that was already built for this purpose:
```python
def view_garage(self):
    if not self.cars:
        print("No cars in the garage yet.")
        return
    for car in self.cars:
        print(car.display_info())
        print("---")
```

### 9. `tune_up` / `Retire`: checking `!=` instead of `==`, returning on the first mismatch
```python
for j in self.cars:
    if j.number != car.number:
        print("this car is not in the garage !")
        return   # quits after checking just ONE car, even if the real match is later in the list
```
**Fix:** search for a **match** and only report "not found" after the *entire* list has been checked:
```python
for j in self.cars:
    if j.number == car.number:
        # ... do the work ...
        return
print("this car is not in the garage")
```

### 10. `Car.self.name` — invalid syntax
```python
Car.self.name = "NewName"   # AttributeError: type object 'Car' has no attribute 'self'
```
**Fix:** `self` is a local variable that only exists inside a method, referring to whichever object called it — it's not something you reach through the class name. Inside a loop like `for j in self.cars:`, the object to edit is `j`:
```python
j.name = "NewName"
```

### 11. `==` used instead of `=` (comparison instead of assignment)
```python
j.number == int(input("Enter the new number:"))   # compares, discards the result — nothing gets saved
```
**Fix:** a single `=` to actually assign the value:
```python
j.number = int(input("Enter the new number:"))
```

### 12. Missing colon after an `elif` condition
```python
elif editing_part == "age"        # SyntaxError: expected ':'
     j.age = int(input(...))
```
**Fix:** every `if`/`elif`/`else` line must end with `:`.

### 13. `search` method calling `super().__init__()` for no reason
```python
def search(self, number, name):
    cars = super().__init__(number, name)   # Garage doesn't inherit from Car — nothing to call here
```
**Fix:** rewrite as a plain keyword search over the existing car list:
```python
def search(self, keyword):
    keyword = str(keyword).strip().lower()
    for car in self.cars:
        if keyword in car.name.lower() or keyword == str(car.number).lower():
            print(car.display_info())
```

### 14. Comparing menu choice as an int against a string
```python
choice = input("Choose an option: ")
if choice == 1:      # always False — input() returns a STRING "1", not the number 1
```
**Fix:** compare against the string `"1"`, or explicitly convert with `int(choice)` first (and wrap that in a try/except in case of non-numeric input).

### 15. Variable scope: `garage` created inside one function, used outside it
```python
def main_menu():
    garage = Garage()      # only exists inside main_menu

while True:
    check_in(garage)       # NameError: 'garage' is not defined — this is OUTSIDE main_menu
```
**Fix:** the entire `while True:` loop needs to live *inside* `main_menu()`, so `garage` stays alive for the whole session. Also remember to actually call `main_menu()` at the bottom of the file — defining a function doesn't run it.

### 16. `check_in`'s `else` branch didn't stop execution
```python
else:
    print("Invalid inputs. check in cancelled")
# missing return here!
garage.check_in(new_car)   # crashes: new_car was never created
```
**Fix:** add `return` immediately after handling the error case, so the code below (which assumes success) never runs on a failed path.

### 17. Recursive infinite loop
```python
def view_garage():
    sense = view_garage()   # calls itself forever — freezes the program
    print(sense)
```
**Fix:** call the actual `Garage` method that does the real work (`garage.view_garage()`), not a free function that calls itself.

### 18. Method name mismatch between call site and definition
```python
garage.check_in(new_car)     # called this...
def check_in_car(self, car): # ...but the method is actually named this
```
**Fix:** make sure the name used to call a method exactly matches how it was defined.

### 19. `Retire`: typo `remover` instead of `remove`
```python
self.cars.remover(car)   # AttributeError: no such method
```
**Fix:** `self.cars.remove(car)` — remove is a built-in Python list method, remover is not.

### 20. `tune_up` printed "not in the garage" even after successfully editing
```python
for j in self.cars:
    if j.number == car.number:
        # ...edit fields...
        # missing return here
print("this car is not in the garage")   # runs even after a successful edit
```
**Fix:** `return` immediately after a successful edit so the "not found" message (meant for the loop finishing with no match) doesn't run afterward.

## Persistence Notes

- Data is saved to JSON via `to_dict()` on each car, which includes a `"type"` field (`"Racer"` or `"Support"`).
- On load, that `"type"` field is what allows `Garage.load_from_file()` to reconstruct the correct subclass (`Racer_car` vs `Support_Vehicle`) instead of losing the class hierarchy and falling back to plain dictionaries.
- `os.path.exists(self.data_file)` is checked before attempting to open the file, so the very first run (before any file exists) doesn't crash with `FileNotFoundError`.
- `save_to_file()` is called at the end of every state-changing operation (check-in, tune-up, retire) rather than only once at program exit, per the task's "updated directly after any changes" requirement.

## Lessons Learned

- **Polymorphism only works if method names match exactly** across subclasses — a single casing mismatch (`Preformance_score` vs `preformance_score`) is enough to break it.
- **Loop-and-search bugs are almost always about `==` vs `!=`, and where `return`/`append` sits relative to the loop.** Checking for a *mismatch* and bailing out early is a very different (and usually wrong) thing from checking for a *match* and confirming "not found" only once the whole list has been searched.
- **Encapsulation isn't just "use properties for some fields"** — every field that could be set to something invalid needs its own setter, or the validation is only partially enforced.
- **`self` is not reachable via the class name** (`Car.self.x` is never valid) — it only exists as a parameter name inside a method, referring to the specific object that called it.
