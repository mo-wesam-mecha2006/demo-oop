
import json
import os

DATA_FILE = "garage_data.json"


class Car:
    def __init__(self, number, name, age, type, RacingTeam, speed, capacity):
        self.number = number
        self.name = name
        self.age = age
        self.type = type
        self.RacingTeam = RacingTeam
        self.speed = speed
        self.capacity = capacity

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Speed must be positive.")
        self._speed = value

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Capacity must be positive.")
        self._capacity = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        value = int(value)
        if value <= 0:
            raise ValueError("Age must be positive.")
        self._age = value

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        if str(value).strip() == "":
            raise ValueError("Car Number cannot be empty.")
        self._number = str(value).strip()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not str(value).strip():
            raise ValueError("Name cannot be empty.")
        self._name = str(value).strip()

    @property
    def RacingTeam(self):
        return self._RacingTeam

    @RacingTeam.setter
    def RacingTeam(self, value):
        if not value or not str(value).strip():
            raise ValueError("Racing Team cannot be empty.")
        self._RacingTeam = str(value).strip()

    def display_info(self):
        return (
            f'Number = {self.number} \n'
            f' Name = {self.name} \n'
            f' Age = {self.age} \n'
            f' Type = {self.type} \n'
            f' Racing team = {self.RacingTeam} \n'
            f' Speed = {self.speed} \n'
            f' Capacity = {self.capacity} '
        )

    def to_dict(self):
        return {
            "number": self.number, "name": self.name, "age": self.age,
            "type": self.type, "RacingTeam": self.RacingTeam,
            "speed": self.speed, "capacity": self.capacity,
        }



class Racer_car(Car):
    def __init__(self, number, name, age, type, RacingTeam, speed, capacity,
                 races_completed, laps_completed):
        super().__init__(number, name, age, type, RacingTeam, speed, capacity)
        self.races_completed = races_completed
        self.laps_completed = laps_completed

    @property
    def races_completed(self):
        return self._races_completed

    @races_completed.setter
    def races_completed(self, value):
        value = int(value)
        if value < 0:
            raise ValueError("Races Completed cannot be negative.")
        self._races_completed = value

    @property
    def laps_completed(self):
        return self._laps_completed

    @laps_completed.setter
    def laps_completed(self, value):
        value = int(value)
        if value < 0:
            raise ValueError("Laps Completed cannot be negative.")
        self._laps_completed = value

    def preformance_score(self):
        return (self.speed * 10) + (self.capacity * 1)

    def display_info(self):
        base_info = super().display_info()
        return (f'{base_info} \n Races completed = {self.races_completed}'
                f' \n Laps completed = {self.laps_completed}'
                f' \n Performance Score = {self.preformance_score():.2f}')

    def to_dict(self):
        data = super().to_dict()
        data["races_completed"] = self.races_completed
        data["laps_completed"] = self.laps_completed
        return data


class Support_Vehicle(Car):
    def __init__(self, number, name, age, type, RacingTeam, speed, capacity,
                 crew_size, reliability_rating):
        super().__init__(number, name, age, type, RacingTeam, speed, capacity)
        self.crew_size = crew_size
        self.reliability_rating = reliability_rating

    @property
    def crew_size(self):
        return self._crew_size

    @crew_size.setter
    def crew_size(self, value):
        value = int(value)
        if value < 0:
            raise ValueError("Crew Size cannot be negative.")
        self._crew_size = value

    @property
    def reliability_rating(self):
        return self._reliability_rating

    @reliability_rating.setter
    def reliability_rating(self, value):
        value = float(value)
        if not (0 <= value <= 10):
            raise ValueError("Reliability Rating must be between 0 and 10.")
        self._reliability_rating = value

    def preformance_score(self):
        return (self.speed * 5) + (self.capacity * 5)

    def display_info(self):
        base_info = super().display_info()
        return (f'{base_info} \n Crew size = {self.crew_size}'
                f' \n Reliability = {self.reliability_rating}'
                f' \n Performance Score = {self.preformance_score():.2f}')

    def to_dict(self):
        data = super().to_dict()
        data["crew_size"] = self.crew_size
        data["reliability_rating"] = self.reliability_rating
        return data



class Garage:
    def __init__(self, data_file=DATA_FILE):
        self.cars = []
        self.data_file = data_file
        self.load_from_file()

    
    def check_in_car(self, car):
        for i in self.cars:
            if i.number == car.number:
                raise ValueError("this car number already exists.")
        self.cars.append(car)
        print("Car Checked In Successfully!")
        self.save_to_file()

    def view_garage(self):
        if not self.cars:
            print("there is no cars in the garage yet")
            return
        for car in self.cars:
            print(car.display_info())
            print("---")

    def tune_up(self, car_number):
        for j in self.cars:
            if j.number == car_number:
                print(j.display_info())
                editing_part = str(input(
                    "Enter the part you want to edit, please enter in lowercase: "
                )).strip().lower()
                try:
                    if editing_part == 'name':
                        j.name = str(input("Enter the new name: "))
                    elif editing_part == 'age':
                        j.age = int(input("Enter the new age: "))
                    elif editing_part == 'racing team':
                        j.RacingTeam = str(input("Enter the new racing team: "))
                    elif editing_part == 'speed':
                        j.speed = float(input("Enter the new speed: "))
                    elif editing_part == 'capacity':
                        j.capacity = float(input("Enter the new capacity: "))
                    elif editing_part == 'races_completed' and isinstance(j, Racer_car):
                        j.races_completed = int(input("Enter the new races completed: "))
                    elif editing_part == 'laps_completed' and isinstance(j, Racer_car):
                        j.laps_completed = int(input("Enter the new laps completed: "))
                    elif editing_part == 'crew_size' and isinstance(j, Support_Vehicle):
                        j.crew_size = int(input("Enter the new crew size: "))
                    elif editing_part == 'reliability_rating' and isinstance(j, Support_Vehicle):
                        j.reliability_rating = float(input("Enter the new reliability rating: "))
                    else:
                        print("Invalid field name.")
                        return
                    print("Car updated successfully!")
                    self.save_to_file()
                except ValueError as e:
                    print(f"Error: {e}")
                return
        print("this car is not in the garage")

    def retire(self, car_number):
        for car in self.cars:
            if car.number == car_number:
                self.cars.remove(car)
                print("Car retired successfully.")
                self.save_to_file()
                return
        print("this car is not in the garage")

    def search(self, keyword):
        keyword = str(keyword).strip().lower()
        found_any = False
        for car in self.cars:
            if keyword in car.name.lower() or keyword == str(car.number).lower():
                print(car.display_info())
                print("---")
                found_any = True
        if not found_any:
            print("not found")

    def report(self):
        if not self.cars:
            print("No cars in the garage yet.")
            return

        total_cars = len(self.cars)
        total_score = sum(car.preformance_score() for car in self.cars)
        average_score = total_score / total_cars

        team_counts = {}
        for car in self.cars:
            if car.RacingTeam in team_counts:
                team_counts[car.RacingTeam] += 1
            else:
                team_counts[car.RacingTeam] = 1

        print("--- Garage Report ---")
        print(f"Total cars checked in: {total_cars}")
        print(f"Average performance score: {average_score:.2f}")
        print("Cars per racing team:")
        for team, count in team_counts.items():
            print(f"  {team}: {count}")

    
    def save_to_file(self):
        payload = [car.to_dict() for car in self.cars]
        with open(self.data_file, "w") as f:
            json.dump(payload, f, indent=2)

    def load_from_file(self):
        if not os.path.exists(self.data_file):
            return
        with open(self.data_file, "r") as f:
            try:
                payload = json.load(f)
            except json.JSONDecodeError:
                return

        for entry in payload:
            try:
                if entry.get("type") == "Racer":
                    car = Racer_car(
                        entry["number"], entry["name"], entry["age"], entry["type"],
                        entry["RacingTeam"], entry["speed"], entry["capacity"],
                        entry.get("races_completed", 0), entry.get("laps_completed", 0),
                    )
                elif entry.get("type") == "Support":
                    car = Support_Vehicle(
                        entry["number"], entry["name"], entry["age"], entry["type"],
                        entry["RacingTeam"], entry["speed"], entry["capacity"],
                        entry.get("crew_size", 0), entry.get("reliability_rating", 0),
                    )
                else:
                    continue
                self.cars.append(car)
            except (KeyError, ValueError):
                continue  



def check_in(garage):
    try:
        number = input("Enter car number: ")
        name = input("Enter name: ")
        age = int(input("Enter age: "))
        RacingTeam = input("Enter racing team: ")
        speed = float(input("Enter speed: "))
        capacity = float(input("Enter capacity: "))
        car_type = input("Type (racer/support): ").strip().lower()

        if car_type == "racer":
            races_completed = int(input("Enter the races completed: "))
            laps_completed = int(input("Enter the laps completed: "))
            new_car = Racer_car(number, name, age, "Racer", RacingTeam, speed, capacity,
                                 races_completed, laps_completed)
        elif car_type == "support":
            crew_size = int(input("Enter the crew size: "))
            reliability_rating = float(input("Enter the reliability rating: "))
            new_car = Support_Vehicle(number, name, age, "Support", RacingTeam, speed, capacity,
                                       crew_size, reliability_rating)
        else:
            print("Invalid type. Check-in cancelled.")
            return

        garage.check_in_car(new_car)

    except ValueError as e:
        print(f"Error: {e}. Check-in cancelled.")


def retire_flow(garage):
    number = input("Enter car number to retire: ")
    confirm = input(f"Are you sure you want to retire car {number}? (y/n): ").strip().lower()
    if confirm == "y":
        garage.retire(number)
    else:
        print("Retire cancelled.")


def tune_up_flow(garage):
    number = input("Enter car number to tune up: ")
    garage.tune_up(number)


def search_flow(garage):
    keyword = input("Search by name or car number: ")
    garage.search(keyword)



def main_menu():
    garage = Garage()

    while True:
        print("\n--- Radiator Springs Garage ---")
        print("1. Check In")
        print("2. View Garage")
        print("3. Tune-Up")
        print("4. Retire")
        print("5. Search")
        print("6. Report")
        print("7. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            check_in(garage)
        elif choice == "2":
            garage.view_garage()
        elif choice == "3":
            tune_up_flow(garage)
        elif choice == "4":
            retire_flow(garage)
        elif choice == "5":
            search_flow(garage)
        elif choice == "6":
            garage.report()
        elif choice == "7":
            print("Goodbye, and ka-chow!")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main_menu()