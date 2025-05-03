import csv
import random
from faker import Faker
import csv

fake = Faker()

NUM_PASSENGERS = 10000
NUM_PILOTS = 1000
NUM_FLIGHTS = 5000

aids = []

passengers = []
for pid in range(1, NUM_PASSENGERS + 1):
    passengers.append([
        pid,
        fake.first_name(),
        fake.last_name(),
        fake.email(),
        fake.phone_number(),
        random.randint(10000000, 99999999)
    ])


pilots = []
for pid in range(1, NUM_PILOTS + 1):
    with open('Airline.csv', 'r') as f:
        reader = csv.reader(f)
        airlines = list(reader)

    aid_values = [row[2] for row in airlines[1:]]

    aid = random.choice(aid_values)
    pilots.append([pid, fake.name(), random.randint(1, 40), aid])

flights = []
for fid in range(1, NUM_FLIGHTS + 1):
    with open('Airline.csv', 'r') as f:
        reader = csv.reader(f)
        airlines = list(reader)

    aid_values = [row[0] for row in airlines[1:]]

    aid = random.choice(aid_values)

    with open('Airport.csv', 'r') as f:
        reader = csv.reader(f)
        airports = list(reader)
    airport_codes = [row[0] for row in airports[1:]]
    origin, destination = random.sample(airport_codes, 2)

    aid = random.choice(aid_values)
    flights.append([
        fid,
        aid,
        origin,
        destination,
        fake.date_time_this_year().isoformat(),
        fake.date_time_this_year().isoformat(),
        "Boeing-7" + str(random.randint(10, 99)),
        random.choice(["On-Time","On-Time","On-Time","On-Time","On-Time", "Delayed","Delayed", "Cancelled"]),
        random.randint(0, 300)
    ])

def write_csv(filename, headers, data):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

write_csv('Passenger.csv', ['passID', 'firstName', 'lastName', 'email', 'phone', 'passportNumber'], passengers)
write_csv('Pilot.csv', ['pilotID', 'name', 'years', 'aid'], pilots)
write_csv('Flight.csv', ['fid', 'flightNumber', 'aid', 'originCode', 'destinationCode', 'departureTime', 'arrivalTime', 'aircraftModel', 'status', 'availableSeats'], flights)
