import heapq
from collections import defaultdict, OrderedDict

def online():
    l=[]
    with open('input.txt') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            a=lines[i].replace("\n","")
            l.append(a)
        return l

class Car:
    def __init__(self, registration_number, age):
        self.registration_number = registration_number
        self.age = age

    def __str__(self):
        return 'Car [registration_number=" + self.registration_number + ", age=" + self.age + "]'


class ParkingLot:
    def __init__(self, total_slots):
        self.registration_slot_mapping = dict()
        self.age_registration_mapping = defaultdict(list)
        # we need to maintain the orders of cars while showing 'status'
        self.slot_car_mapping = OrderedDict()

        # initialize all slots as free
        self.available_parking_lots = []
        # Using min heap as this will always give minimun slot number in O(1) time
        for i in range(1, total_slots + 1):
            heapq.heappush(self.available_parking_lots, i)

    def status(self):
        for slot, car in self.slot_car_mapping.items():
            print("Slot no: {} {}".format(slot, car))

    def get_nearest_slot(self):
        return heapq.heappop(self.available_parking_lots) if self.available_parking_lots else None

    def free_slot(self, slot_to_be_freed):
        found = None
        ag= None
        for registration_no, slot in self.registration_slot_mapping.items():
            if slot == slot_to_be_freed:
                found = registration_no
        for age, registration_no in self.age_registration_mapping.items():
            for ir in registration_no:
                if ir == found:
                    ag= age
        
        # Cleanup from all cache
        if found:
            print("Slot number "+str(slot_to_be_freed)+" vacated, the car with vehicle registration number "+found+" left the space, the driver of the car was of age "+str(ag))
            del self.registration_slot_mapping[found]
            car_to_leave = self.slot_car_mapping[slot_to_be_freed]
            self.age_registration_mapping[car_to_leave.age].remove(found)
            del self.slot_car_mapping[slot_to_be_freed]
        else:
            print("slot is not in use")
    
    def slot_by_reg(self, regno):
        for registration_no, slot in self.registration_slot_mapping.items():
            if registration_no == regno:
                return slot

    def park_car(self, car):
        slot_no = self.get_nearest_slot()
        if slot_no is None:
            print("Sorry, parking lot is full")
            return
        self.slot_car_mapping[slot_no] = car
        self.registration_slot_mapping[car.registration_number] = slot_no
        self.age_registration_mapping[car.age].append(car.registration_number)
        return(slot_no)


    def get_registration_nos_by_age(self, age):
        return self.age_registration_mapping[age]


    def get_slot_numbers_by_age(self, age):
        return [self.registration_slot_mapping[reg_no] for reg_no in self.age_registration_mapping[age]]


l=online()
for i in range(len(l)):
    st=l[i] # Taking input line by line  
    length=len(st)

    # Creating a parking lot
    if("Create_parking_lot" in l[i]):
        n=st[19:length+1]
        parking_lot = ParkingLot(int(n))
        print("Created parking of "+n+" slots")

    # Parking cars in parking lot at the nearest slot available
    elif("Park" in l[i]):
        rno=st[5:18]
        age=st[-2:]
        car = Car(rno, age)
        s_no=parking_lot.park_car(car)
        print("Car with vehicle registration number "+rno+" has been parked at slot number "+str(s_no))


    # Query - Cars whos drivers age is specified is parked at which slots
    elif("Slot_numbers_for_driver_of_age" in l[i]):
        age=st[-2:]
        s_no=parking_lot.get_slot_numbers_by_age(age)
        print("{}".format(s_no))

    # Details of car which leaves the parking lot
    elif("Leave" in l[i]):
        slot_no_to_be_freed=int(st[6:length])
        parking_lot.free_slot(slot_no_to_be_freed)
        heapq.heappush(parking_lot.available_parking_lots, slot_no_to_be_freed)
        
    # At which slot a particula car is parked
    elif("Slot_number_for_car_with_number" in l[i]):
        regno=st[32:]
        s_no =  parking_lot.slot_by_reg(regno)
        print(s_no)

    # List of vechile registration numbers for a particular age of driver
    elif("Vehicle_registration_number_for_driver_of_age" in l[i]):
        age=st[-2:]
        registration_numbers = parking_lot.get_registration_nos_by_age(age)
        print("{}".format(registration_numbers))

    # If command does not  match with any of the mentioned commands
    else:
        print("Sorry for the enconvinence, this information is not available right now!!")