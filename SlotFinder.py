from datetime import datetime

class ChargingStation:
    def __init__(self, name, location, connector_types, total_slots):
        self.name = name
        self.location = location
        self.connector_types = connector_types
        self.total_slots = total_slots
        self.booked_slots = {}  # Dictionary to hold booked slots with datetime keys

    def display_info(self):
        print(f"Station Name: {self.name}")
        print(f"Location: {self.location}")
        print(f"Connector Types: {', '.join(self.connector_types)}")
        print(f"Available Slots: {self.get_total_available_slots()} (for any date/time)")
        print("-" * 30)
    
    def get_total_available_slots(self):
        # Calculate total available slots across all time slots
        total_booked = sum(self.booked_slots.values())
        return self.total_slots - total_booked

    def get_available_slots(self, date_time=None):
        # Calculate available slots for a specific date and time
        if date_time and date_time in self.booked_slots:
            return self.total_slots - self.booked_slots[date_time]
        return self.total_slots
    
    def book_slot(self, date_time, connector_type):
        if connector_type not in self.connector_types:
            print(f"Connector type '{connector_type}' is not supported at this station.")
            return
        
        if date_time in self.booked_slots:
            if self.booked_slots[date_time] < self.total_slots:
                self.booked_slots[date_time] += 1
                print(f"Slot booked successfully at {self.name} on {date_time} with connector '{connector_type}'.")
            else:
                print("No available slots at this station for the selected date and time.")
        else:
            self.booked_slots[date_time] = 1
            print(f"Slot booked successfully at {self.name} on {date_time} with connector '{connector_type}'.")

    def show_booked_slots(self):
        if not self.booked_slots:
            print(f"No slots booked at {self.name}.")
        else:
            print(f"Booked slots at {self.name}:")
            for date_time, slots in self.booked_slots.items():
                print(f"- {date_time}: {slots} slot(s) booked")
        print(f"Vacant slots: {self.get_total_available_slots()}")
        print("-" * 30)

def filter_stations(stations, location=None, connector_type=None):
    filtered_stations = stations
    
    if location:
        filtered_stations = [station for station in filtered_stations if station.location == location]
    
    if connector_type:
        filtered_stations = [station for station in filtered_stations if connector_type in station.connector_types]
    
    return filtered_stations

def main():
    stations = [
        ChargingStation("Green Charge", "New York", ["Type1", "Type2"], 5),
        ChargingStation("Eco Power", "San Francisco", ["Type2", "Type3"], 3),
        ChargingStation("ChargeUp", "Los Angeles", ["Type1", "Type3"], 2),
    ]
    
    print("Welcome to the EV Charging Station Finder and Slot Booking System\n")
    
    while True:
        print("1. Find Charging Station")
        print("2. Book a Slot")
        print("3. Show Booked and Vacant Slots")
        print("4. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            location = input("Enter location (or leave blank to skip): ")
            connector_type = input("Enter connector type (or leave blank to skip): ")
            
            results = filter_stations(stations, location, connector_type)
            
            if results:
                print("\nAvailable Charging Stations:")
                for station in results:
                    station.display_info()
            else:
                print("No stations found with the specified filters.")
        
        elif choice == '2':
            station_name = input("Enter the name of the station where you want to book a slot: ")
            station = next((s for s in stations if s.name == station_name), None)
            
            if station:
                connector_type = input(f"Enter the connector type (Available: {', '.join(station.connector_types)}): ")
                
                if connector_type not in station.connector_types:
                    print("Invalid connector type. Please try again.")
                    continue
                
                if station.get_total_available_slots() > 0:
                    date_time_str = input("Enter the date and time for booking (YYYY-MM-DD HH:MM): ")
                    
                    try:
                        # Convert the input string to a datetime object
                        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
                        
                        # Check available slots before booking
                        available_slots = station.get_available_slots(date_time)
                        
                        if available_slots > 0:
                            station.book_slot(date_time, connector_type)
                        else:
                            print("No available slots at the selected date and time.")
                    except ValueError:
                        print("Invalid date and time format. Please try again.")
                else:
                    print("No available slots at this station.")
            else:
                print("Station not found.")
        
        elif choice == '3':
            print("\nCurrently Booked and Vacant Slots:\n")
            for station in stations:
                station.show_booked_slots()
        
        elif choice == '4':
            print("Thank you for using the system.")
            break
        
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
