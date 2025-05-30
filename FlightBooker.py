import mysql.connector
from datetime import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="aviationDB"
)
cursor = conn.cursor()

def find_passenger_id(first, last):
    cursor.execute("SELECT passID FROM Passenger WHERE firstName=%s AND lastName=%s", (first, last))
    result = cursor.fetchone()
    return result[0] if result else None

def get_loyalty_info(passID):
    cursor.execute("""
        SELECT l.passID, l.aid, l.membershipNumber, l.tier, l.points, a.name
        FROM loyaltymember l JOIN Airline a ON l.aid = a.aid
        WHERE l.passID = %s
    """, (passID,))
    return cursor.fetchall()

def list_bookings(passID):
    cursor.execute("""
        SELECT b.fid, f.originCode, f.destinationCode, f.departureTime, b.seatNumber, b.class
        FROM Booking b
        JOIN Flight f ON b.fid = f.fid
        WHERE b.passID = %s
    """, (passID,))
    return cursor.fetchall()

def list_available_flights():
    cursor.execute("""
        SELECT fid, originCode, destinationCode, departureTime, availableSeats, price
        FROM Flight
        JOIN Booking USING(fid)
        WHERE availableSeats > 0 AND departureTime > NOW()
        LIMIT 5
    """)
    return cursor.fetchall()

def book_flight(passID, fid, seat, booking_class, price):
    today = datetime.today().strftime('%Y-%m-%d')
    cursor.execute("""
        INSERT INTO Booking (passID, fid, bookingDate, seatNumber, class, price, paymentStatus, checkInStatus)
        VALUES (%s, %s, %s, %s, %s, %s, 'Paid', 'Not Checked In')
    """, (passID, fid, today, seat, booking_class, price))
    
    cursor.execute("UPDATE Flight SET availableSeats = availableSeats - 1 WHERE fid = %s", (fid,))
    cursor.execute("UPDATE loyaltymember SET points = points + %s WHERE passID = %s", (int(price), passID))

    tiers = {0: "Standard", 30000: "Silver", 50000: "Gold", 70000: "Platinum"}
    pts = int(get_loyalty_info(passID)[0][4])
    memTier = "Standard"
    for i, (key,value) in enumerate(tiers.items()):
        if (pts + int(price)) >= key:
            memTier = value

    cursor.execute("UPDATE loyaltymember SET tier = %s WHERE passID = %s", (str(memTier), passID))
    conn.commit()

first = input("Enter passenger's first name: ")
last = input("Enter passenger's last name: ")

passID = find_passenger_id(first, last)
if passID:
    print("\n--- Loyalty Info ---")
    for info in get_loyalty_info(passID):
        print(f"Airline: {info[5]}, Membership #: {info[2]}, Tier: {info[3]}, Points: {info[4]}, PassID: {info[0]}")
    
    print("\n--- Booked Flights ---")
    for b in list_bookings(passID):
        print(f"Flight ID: {b[0]}, {b[1]} -> {b[2]}, Depart: {b[3]}, Seat: {b[4]}, Class: {b[5]}")

    print("\n--- Available Flights ---")
    flights = list_available_flights()
    for f in flights:
        print(f"ID: {f[0]}, {f[1]} -> {f[2]}, Depart: {f[3]}, Seats: {f[4]}, Price: ${f[5]}")

    fid = int(input("\nEnter Flight ID to book: "))
    seat = input("Enter Seat Number: ")
    booking_class = input("Enter Class (Economy/Business): ")
    price = float(input("Enter Price: "))
    
    book_flight(passID, fid, seat, booking_class, price)
    print("\nBooking successful and loyalty points updated.")
else:
    print("Error: Passenger not found.")

cursor.close()
conn.close()
