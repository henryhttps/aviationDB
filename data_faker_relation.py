import csv
import random
from faker import Faker
from datetime import datetime

fake = Faker()

# Load data
def load_csv(path):
    with open(path, 'r') as f:
        return list(csv.reader(f))[1:] 

flights = load_csv('Flight.csv')
pilots = load_csv('Pilot.csv')
passengers = load_csv('Passenger.csv')
airlines = load_csv('Airline.csv')
airports = load_csv('Airport.csv')

flight_ids = [row[0] for row in flights]
pilot_ids = [row[0] for row in pilots]
passenger_ids = [row[0] for row in passengers]
airline_ids = [row[0] for row in airlines]
airport_codes = [row[0] for row in airports]

service_types = ['Passenger', 'Cargo', 'Mixed']
operating_days = ['Mon-Fri', 'Weekends', 'Daily', 'Mon, Wed, Fri', 'Tue, Thu']

serves = []
for _ in range(3000):
    aid = random.choice(airline_ids)
    fid = random.choice(flight_ids)
    serves.append([
        aid,
        fid,
        random.choice(service_types),
        random.choice(operating_days)
    ])

roles = ['Captain', 'First Officer']
flies = []
for _ in range(5000):
    pilotID = random.choice(pilot_ids)
    fid = random.choice(flight_ids)
    flies.append([
        pilotID,
        fid,
        random.choice(roles)
    ])

partner = []
for _ in range(1500):
    aid = random.choice(airline_ids)
    code = random.choice(airport_codes)
    partner.append([aid, code])

worksfor = []
for _ in range(2000):
    pilotID = random.choice(pilot_ids)
    aid = random.choice(airline_ids)
    years = random.randint(1, 40)
    worksfor.append([pilotID, aid, years])

classes = ['Economy', 'Business', 'First']
statuses = ['Paid', 'Pending', 'Cancelled']
checkin = ['Checked-in', 'Not Checked-in']

booking = []
for _ in range(10000):
    passID = random.choice(passenger_ids)
    fid = random.choice(flight_ids)
    bookingDate = fake.date_this_year().isoformat()
    seatNumber = f"{random.randint(1, 50)}{random.choice('ABCDEF')}"
    flight_class = random.choice(classes)
    price = round(random.uniform(50, 1500), 2)
    paymentStatus = random.choice(statuses)
    checkInStatus = random.choice(checkin)
    booking.append([
        passID, fid, bookingDate, seatNumber, flight_class, price, paymentStatus, checkInStatus
    ])

tiers = ['Silver', 'Gold', 'Platinum', 'Diamond']
loyalty = []
for _ in range(5000):
    passID = random.choice(passenger_ids)
    aid = random.choice(airline_ids)
    membershipNumber = random.randint(100000, 999999)
    tier = random.choice(tiers)
    points = random.randint(100, 100000)
    loyalty.append([passID, aid, membershipNumber, tier, points])

def write_csv(filename, headers, data):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

write_csv('Serves.csv', ['aid', 'fid', 'serviceType', 'operatingDays'], serves)
write_csv('Flies.csv', ['pilotID', 'fid', 'role'], flies)
write_csv('Partner.csv', ['aid', 'code'], partner)
write_csv('WorksFor.csv', ['pilotID', 'aid', 'years'], worksfor)
write_csv('Booking.csv', ['passID', 'fid', 'bookingDate', 'seatNumber', 'class', 'price', 'paymentStatus', 'checkInStatus'], booking)
write_csv('LoyaltyMember.csv', ['passID', 'aid', 'membershipNumber', 'tier', 'points'], loyalty)
