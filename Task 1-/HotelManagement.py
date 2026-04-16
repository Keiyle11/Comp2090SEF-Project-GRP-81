
from datetime import datetime
from abc import ABC, abstractmethod

class Room:
    def __init__(self, room_number, price, capacity):
        self.room_number = room_number
        self.price = price
        self.capacity = capacity
        self.is_occupied = False
    
    def calculate_price(self):
        return self.price
    
    def __str__(self):
        return f"Room {self.room_number} - ${self.price}/night"
    
class Deluxe(Room):
    def calculate_price(self):
        return self.price * 1.20

class DiscountRoom(Room):
    def calculate_price(self):
        return self.price * 0.85

class PremiumRoom(Room):
    def calculate_price(self):
        return self.price * 1.30
    
class DiscountCoupon(ABC):
    def __init__(self, code, description):
        self.code = code
        self.description = description
        self.is_used = False
    
    @abstractmethod
    def apply_discount(self, total_cost, nightly_rate=None, nights=None):
        pass
    
    @abstractmethod
    def get_discount_info(self):
        pass
    
    def use_coupon(self):
        if not self.is_used:
            self.is_used = True
            return True
        return False
    
    def __str__(self):
        status = "Used" if self.is_used else "Available"
        return f"Coupon '{self.code}': {self.description} ({status})"

class PercentageCoupon(DiscountCoupon):
    def __init__(self, code, description, percentage):
        super().__init__(code, description)
        self.percentage = percentage
    
    def apply_discount(self, total_cost, nightly_rate=None, nights=None):
        discount_amount = total_cost * (self.percentage / 100)
        return total_cost - discount_amount
    
    def get_discount_info(self):
        return f"{self.percentage}% off"

class FixedAmountCoupon(DiscountCoupon):
    def __init__(self, code, description, amount_off):
        super().__init__(code, description)
        self.amount_off = amount_off
    
    def apply_discount(self, total_cost, nightly_rate=None, nights=None):
        return max(0, total_cost - self.amount_off)
    
    def get_discount_info(self):
        return f"${self.amount_off} off"

class FreeNightCoupon(DiscountCoupon):
    def __init__(self, code, description):
        super().__init__(code, description)
    
    def apply_discount(self, total_cost, nightly_rate=None, nights=None):
        if nights and nights >= 2 and nightly_rate:
            return total_cost - nightly_rate
        return total_cost
    
    def get_discount_info(self):
        return "One free night"

class Guest:
    def __init__(self, guest_id, name, email, phone):
        self.guest_id = guest_id
        self.name = name
        self.email = email
        self.phone = phone
        self.coupons = []
    
    def add_coupon(self, coupon):
        self.coupons.append(coupon)
        print(f"  → Coupon added: {coupon}")
    
    def get_available_coupons(self):
        return [c for c in self.coupons if not c.is_used]
    
    def __str__(self):
        return f"{self.name} (ID: {self.guest_id})"

class Reservation:
    def __init__(self, reservation_id, guest, room, check_in, check_out, discount_coupon=None):
        self.reservation_id = reservation_id
        self.guest = guest
        self.room = room
        self.check_in = check_in
        self.check_out = check_out
        self.status = "Confirmed"
        self.discount_coupon = discount_coupon
        
        nights = (check_out - check_in).days
        nightly_rate = room.calculate_price()
        self.original_total = nights * nightly_rate
        self.total_cost = self.original_total
        
        if discount_coupon and not discount_coupon.is_used:
            self.total_cost = discount_coupon.apply_discount(
                self.original_total, 
                nightly_rate=nightly_rate, 
                nights=nights
            )
            discount_coupon.use_coupon()
            print(f"   Coupon '{discount_coupon.code}' applied! Saved: ${self.original_total - self.total_cost:.2f}")
    
    def __str__(self):
        coupon_text = ""
        if self.discount_coupon:
            coupon_text = f" [Coupon: {self.discount_coupon.code}]"
        return f"Reservation #{self.reservation_id}: {self.guest.name} - Room {self.room.room_number} - ${self.total_cost:.2f}{coupon_text}"

class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = []
        self.guests = []
        self.reservations = []
        self.next_reservation_id = 1
        self.next_guest_id = 1
        self.available_coupons = []
    
    def add_room(self, room_number, price, capacity, special_type=None):
        if special_type == "deluxe":
            room = Deluxe(room_number, price, capacity)
        elif special_type == "discount":
            room = DiscountRoom(room_number, price, capacity)
        elif special_type == "premium":
            room = PremiumRoom(room_number, price, capacity)
        else:
            room = Room(room_number, price, capacity)
        
        self.rooms.append(room)
        print(f"Added: {room}")
        if special_type:
            print(f"  ↳ Special pricing applied: {special_type}")
    
    def create_coupon(self, coupon_type, code, description, *args):
        if coupon_type == "percentage":
            percentage = args[0]
            coupon = PercentageCoupon(code, description, percentage)
        elif coupon_type == "fixed":
            amount = args[0]
            coupon = FixedAmountCoupon(code, description, amount)
        elif coupon_type == "freenight":
            coupon = FreeNightCoupon(code, description)
        else:
            print("Invalid coupon type!")
            return None
        
        self.available_coupons.append(coupon)
        print(f"Created: {coupon}")
        return coupon
    
    def give_coupon_to_guest(self, guest_id, coupon_code):
        guest = None
        for g in self.guests:
            if g.guest_id == guest_id:
                guest = g
                break
        
        if not guest:
            print("Guest not found!")
            return False
        
        coupon = None
        for c in self.available_coupons:
            if c.code == coupon_code and not c.is_used:
                coupon = c
                break
        
        if not coupon:
            print(f"Coupon '{coupon_code}' not found or already used!")
            return False
        
        self.available_coupons.remove(coupon)
        guest.add_coupon(coupon)
        return True
    
    def show_all_rooms(self):
        print("\nAll Rooms:")
        if not self.rooms:
            print("No rooms available")
        for room in self.rooms:
            status = "Available" if not room.is_occupied else "Occupied"
            print(f"{room} - {status}")
            
    def show_all_guests(self):
        print("\nAll Guests:")
        if not self.guests:
            print("No Guests Registered")
        for guest in self.guests:
            print(f"{guest}")
    
    def show_available_rooms(self):
        print("\nAvailable Rooms:")
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
    
    def make_reservation(self, guest_id, room_number, check_in, check_out, coupon_code=None):
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
        
        discount_coupon = None
        if coupon_code:
            for coupon in guest.get_available_coupons():
                if coupon.code == coupon_code:
                    discount_coupon = coupon
                    break
            if not discount_coupon:
                print(f"Coupon '{coupon_code}' not found or already used!")
        
        reservation = Reservation(
            self.next_reservation_id, 
            guest, 
            room, 
            check_in, 
            check_out,
            discount_coupon
        )
        
        self.reservations.append(reservation)
        self.next_reservation_id += 1
        room.is_occupied = True
        
        print("Reservation confirmed!")
        print(f"Original total: ${reservation.original_total:.2f}")
        print(f"Final total: ${reservation.total_cost:.2f}")
        print(f"You saved: ${reservation.original_total - reservation.total_cost:.2f}")
        return reservation
    
    def check_out(self, reservation_id):
        for reservation in self.reservations:
            if reservation.reservation_id == reservation_id:
                reservation.status = "Checked Out"
                reservation.room.is_occupied = False
                print(f"Guest {reservation.guest.name} checked out from Room {reservation.room.room_number}")
                return
        print("Reservation not found!")
    
    def show_guest_coupons(self, guest_id):
        guest = None
        for g in self.guests:
            if g.guest_id == guest_id:
                guest = g
                break
        
        if not guest:
            print("Guest not found!")
            return
        
        coupons = guest.get_available_coupons()
        if not coupons:
            print(f"{guest.name} has no available coupons")
        else:
            print(f"\n{guest.name}'s available coupons:")
            for coupon in coupons:
                print(f"  • {coupon}")

def main():
    hotel = Hotel("Grand Hotel")
    startnum = 0
    
    print("\n=== Creating Promotional Coupons ===")
    hotel.create_coupon("percentage", "SAVE10", "10% off your stay", 10)
    hotel.create_coupon("percentage", "SUMMER20", "20% summer special", 20)
    hotel.create_coupon("fixed", "SAVE50", "$50 off total booking", 50)
    hotel.create_coupon("freenight", "FREE1", "One free night", None)
    
    while True:

        print("Hotel Management System")

        print("1. Add Room")
        print("2. Register Guest")
        print("3. Make Reservation")
        print("4. Show All Rooms")
        print("5. Show Available Rooms")
        print("6. Show All Guests")
        print("7. Check Out")
        print("8. View All Reservations")
        print("9. Give Coupon to Guest")
        print("10. Show Guest Coupons")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "0":
            print("End.")
            break
        
        elif choice == "1":
            try:
                Amount = int(input("How many duplicates of this room do you have?: "))
                price = float(input("Price per night: $"))
                capacity = int(input("Capacity (max people): "))
                
                print("\nSpecial pricing options:")
                print("deluxe  - 20% higher price")
                print("discount - 15% lower price")
                print("premium - 30% higher price")
                print("(press Enter for normal pricing)")
                special = input("Special type: ").strip().lower()
                
                if special not in ["deluxe", "discount", "premium", ""]:
                    print("Invalid special type! Using normal pricing.")
                    special = None
                elif special == "":
                    special = None
                
                for x in range(Amount):
                    hotel.add_room(startnum+x, price, capacity, special)
                    
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
                    print("No guests registered!")
                    continue
                
                guest_id = int(input("\nGuest ID: "))
                room_num = int(input("Room Number: "))
                
                use_coupon = input("Apply coupon? (y/n): ").lower()
                coupon_code = None
                if use_coupon == 'y':
                    coupon_code = input("Enter coupon code: ").upper()
                
                check_in = input("Check-in (YYYY-MM-DD): ")
                check_out = input("Check-out (YYYY-MM-DD): ")
                
                check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
                check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
                
                hotel.make_reservation(guest_id, room_num, check_in_date, check_out_date, coupon_code)
            except ValueError as e:
                print(f"Invalid date format! Please use YYYY-MM-DD. Error: {e}")
        
        elif choice == "4":
            hotel.show_all_rooms()
        
        elif choice == "5":
            hotel.show_available_rooms()
            
        elif choice == "6":
           hotel.show_all_guests()
        
        elif choice == "7":
            print("Check Out Guest:")
            try:
                res_id = int(input("Reservation ID: "))
                hotel.check_out(res_id)
            except ValueError:
                print("Invalid reservation ID")
        
        elif choice == "8":
            print("\nAll Reservations")
            if not hotel.reservations:
                print("No reservations yet")
            for res in hotel.reservations:
                nights = (res.check_out - res.check_in).days
                print(f"{res} - {nights} nights - Check-in: {res.check_in.date()}")
        
        elif choice == "9":
            try:
                guest_id = int(input("Guest ID: "))
                coupon_code = input("Coupon code to give: ").upper()
                hotel.give_coupon_to_guest(guest_id, coupon_code)
            except ValueError:
                print("Invalid input!")
        
        elif choice == "10":
            try:
                guest_id = int(input("Guest ID: "))
                hotel.show_guest_coupons(guest_id)
            except ValueError:
                print("Invalid input!")

if __name__ == "__main__":
    main()
