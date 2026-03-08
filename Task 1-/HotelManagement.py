# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 16:56:51 2026

@author: Keiyle
"""

from datetime import datetime

class Room:
    def __init__(self, room_number, price, capacity, room_type):
        self.room_number = room_number
        self.price = price
        self.capacity = capacity
        self.room_type = room_type
        self.is_occupied = False
    
    def __str__(self):
        return f"Room {self.room_number} ({self.room_type}) - ${self.price}/night"

class Guest:
    def __init__(self, guest_id, name, email, phone):
        self.guest_id = guest_id
        self.name = name
        self.email = email
        self.phone = phone
    
    def __str__(self):
        return f"{self.name} (ID: {self.guest_id})"

class Reservation:
    def __init__(self, reservation_id, guest, room, check_in, check_out):
        self.reservation_id = reservation_id
        self.guest = guest
        self.room = room
        self.check_in = check_in
        self.check_out = check_out
        self.status = "Confirmed"
        
        nights = (check_out - check_in).days
        self.total_cost = nights * room.price
    
    def __str__(self):
        return f"Reservation #{self.reservation_id}: {self.guest.name} - Room {self.room.room_number} - {self.status}"

class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = []
        self.guests = []
        self.reservations = []
        self.next_reservation_id = 1
        self.next_guest_id = 1
    
    def add_room(self, room_number, price, capacity, room_type):
        room = Room(room_number, price, capacity, room_type)
        self.rooms.append(room)
        print(f"Added: {room}")
    
    def show_all_rooms(self):
        print("All Rooms:")
        if not self.rooms:
            print("No rooms available")
        for room in self.rooms:
            status = "Available" if not room.is_occupied else "Occupied"
            print(f"{room} - {status}")
    
    def show_available_rooms(self):
        print("Available Rooms:")
        available = [room for room in self.rooms if not room.is_occupied]
        if not available:
            print("No rooms available")
        for room in available:
            print(room)
    
    def register_guest(self, name, email, phone):
        guest = Guest(self.next_guest_id, name, email, phone)
        self.guests.append(guest)
        self.next_guest_id += 1
        print(f"Registered: {guest}")
        return guest
    
    def make_reservation(self, guest_id, room_number, check_in, check_out):
        guest = None
        for g in self.guests:
            if g.guest_id == guest_id:
                guest = g
                break
        
        if not guest:
            print("Guest not found!")
            return None
        
        room = None
        for r in self.rooms:
            if r.room_number == room_number and not r.is_occupied:
                room = r
                break
        
        if not room:
            print("Room not available!")
            return None
        
        reservation = Reservation(
            self.next_reservation_id, 
            guest, 
            room, 
            check_in, 
            check_out
        )
        
        self.reservations.append(reservation)
        self.next_reservation_id += 1
        room.is_occupied = True
        
        print(f"Reservation confirmed! Total: ${reservation.total_cost}")
        return reservation
    
    def check_out(self, reservation_id):
        for reservation in self.reservations:
            if reservation.reservation_id == reservation_id:
                reservation.status = "Checked Out"
                reservation.room.is_occupied = False
                print(f"Guest {reservation.guest.name} checked out from Room {reservation.room.room_number}")
                return
        print("Reservation not found!")

def main():
    hotel = Hotel("Grand Hotel")
    startnum = 0
    while True:
        print("Hotel Management System")
        print("1. Add Room")
        print("2. Register Guest")
        print("3. Make Reservation")
        print("4. Show All Rooms")
        print("5. Show Available Rooms")
        print("6. Check Out")
        print("7. View All Reservations")
        print("0. Exit")

        
        choice = input("Enter your choice: ")
        
        if choice == "0":
            print("End.")
            break
        
        elif choice == "1":
            try:
                Amount = int(input("How many duplicates of this room do you have?: "))
                price = float(input("Price per night: $"))
                capacity = int(input("Capacity (max people): "))
                print("Room Types: Standard, Deluxe, Suite")
                room_type = input("Room Type: ")
                for x in range(Amount):
                    hotel.add_room(startnum+x, price, capacity, room_type)
                    
                startnum = startnum + Amount
            except ValueError:
                print("Invalid input! Please enter numbers correctly.")
        
        elif choice == "2":
            name = input("Guest Name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            hotel.register_guest(name, email, phone)
        
        elif choice == "3":
            try:
                hotel.show_available_rooms()
                
                if not hotel.guests:
                    print("N/A")
                    continue
                
                guest_id = int(input("\nGuest ID: "))
                room_num = int(input("Room Number: "))
                
                check_in = input("Check-in (YYYY-MM-DD): ")
                check_out = input("Check-out (YYYY-MM-DD): ")
                
                check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
                check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
                
                hotel.make_reservation(guest_id, room_num, check_in_date, check_out_date)
            except ValueError as e:
                print(f"Invalid date format! Please use YYYY-MM-DD. Error: {e}")
        
        elif choice == "4":
            hotel.show_all_rooms()
        
        elif choice == "5":
            hotel.show_available_rooms()
        
        elif choice == "6":
            print("Check Out Guest:")
            try:
                res_id = int(input("Reservation ID: "))
                hotel.check_out(res_id)
            except ValueError:
                print("Invalid reservation ID")
        
        elif choice == "7":
            print("\nAll Reservations")
            if not hotel.reservations:
                print("No reservations yet")
            for res in hotel.reservations:
                print(f"{res} - Check-in: {res.check_in.date()} - Check-out: {res.check_out.date()}")

if __name__ == "__main__":
    main()