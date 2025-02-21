# Author: Tiffany Clark
# Date: 2/19/2025
# Description: This program will take the input from the flights.txt file and parse it to find the best flight based on total price (ticket, parking, rental car)


# Imports
from datetime import datetime, timedelta

# Take the input from the flights.txt file and parse it
# The input is in the format of: <day of week, month, day of month, departure time; carrier; price; flight arrival time; day of week, month, day of month, departure time; departure arrival time>
# The output should be the best flight based on total price (ticket, parking, rental car)

# Open and read the file
file = open("flights.txt", "r")
flights = file.readlines()

# Initialize lists to store flight details
departing_NOR_time = []
arriving_LEX_time = []
price = []
carrier = []
departing_LEX_time = []
arriving_NOR_time = []

for flight in flights:
    flight = flight.strip().split(";")  # Remove any trailing newline and split by ';'
    
    # Ensure the flight list has the expected number of elements
    if len(flight) == 6:
        departing_NOR_time.append(flight[0])  # Departure from Norfolk
        carrier.append(flight[1].strip())     # Airline carrier
        price.append(flight[2].strip())       # Price
        arriving_LEX_time.append(flight[3].strip())   # Arrival in Lexington
        departing_LEX_time.append(flight[4].strip())  # Departure from Lexington
        arriving_NOR_time.append(flight[5].strip())   # Arrival back in Norfolk
    else:
        print("Error: Unexpected format in line:", flight)
file.close()

# Second, we need to calculate the total price of each flight
# Take the flight ticket price from the file then use if/else statements to add parking and transportation
# Parking is $12 per day
# If we arrive before 9AM, I need to add $30 for an uber
# If we arrive after 8PM, I need to add $30 for a uber
# Else, $0 for transportation

total_days = []
total_price = []

# Define parking and transportation costs
PARKING_COST_PER_DAY = 12
UBER_COST = 30

for i in range(len(departing_NOR_time)):
    # Parse the departure date and time for Norfolk
    departing_NOR = datetime.strptime(departing_NOR_time[i], "%A, %B %d, %H:%M")
    
    # Extract month and day from departing_NOR for arriving_LEX
    date_part = departing_NOR.strftime("%B %d")  # Extracts "March 21"
    arriving_LEX_time_only = arriving_LEX_time[i].strip()
    arriving_LEX_str = f"{date_part}, {arriving_LEX_time_only}"
    arriving_LEX = datetime.strptime(arriving_LEX_str, "%B %d, %H:%M")
    
    # Parse the departure date and time for Lexington
    departing_LEX = datetime.strptime(departing_LEX_time[i], "%A, %B %d, %H:%M")
    
    # Extract month and day from departing_LEX for arriving_NOR
    date_part_lex = departing_LEX.strftime("%B %d")  # Extracts "March 25"
    arriving_NOR_time_only = arriving_NOR_time[i].strip()
    arriving_NOR_str = f"{date_part_lex}, {arriving_NOR_time_only}"
    arriving_NOR = datetime.strptime(arriving_NOR_str, "%B %d, %H:%M")

    # Adjust for overnight flights (if arrival is earlier than departure, it must be the next day)
    if arriving_LEX < departing_NOR:
        arriving_LEX += timedelta(days=1)
    if arriving_NOR < departing_LEX:
        arriving_NOR += timedelta(days=1)

    # Calculate total days for parking
    total_trip_duration = arriving_NOR - departing_NOR
    total_days_parked = total_trip_duration.days + 1  # Add 1 day to cover partial days
    total_days.append(total_days_parked)

    # Calculate ticket price
    ticket_price = int(price[i])

    # Calculate parking cost
    parking_price = PARKING_COST_PER_DAY * total_days_parked

    # Calculate transportation cost based on arrival time in Lexington
    transportation_price = 0
    if arriving_LEX.hour < 9:  # Before 9 AM
        transportation_price = UBER_COST
    elif arriving_LEX.hour > 20:  # After 8 PM
        transportation_price = UBER_COST

    # Calculate total price
    flight_total = ticket_price + parking_price + transportation_price
    total_price.append(flight_total)

print("Total Days Parked:", total_days)
print("Total Price for Each Flight:", total_price)

# Third, we need to calculate how many days off from work we need to take
# If the departing flight is before 5PM Friday, we need to take that day off
# If the arriving flight is on Monday, we need to take Monday day off
# If the arriving flight is on Tuesday, we need to take Monday and Tuesday off
# Calculate Days Off Needed

days_off_list = []

for i in range(len(departing_NOR_time)):
    days_off = 0

    # Parse the departure date and time for Norfolk
    departing_NOR_str = departing_NOR_time[i] + ", 2025"  # Append the year
    departing_NOR = datetime.strptime(departing_NOR_str, "%A, %B %d, %H:%M, %Y")

    # Extract month and day from departing_NOR for arriving_LEX
    date_part = departing_NOR.strftime("%B %d, %Y")  # Extracts "March 21, 2025"
    arriving_LEX_time_only = arriving_LEX_time[i].strip()
    arriving_LEX_str = f"{date_part}, {arriving_LEX_time_only}"
    arriving_LEX = datetime.strptime(arriving_LEX_str, "%B %d, %Y, %H:%M")

    # Parse the departure date and time for Lexington
    departing_LEX_str = departing_LEX_time[i] + ", 2025"  # Append the year
    departing_LEX = datetime.strptime(departing_LEX_str, "%A, %B %d, %H:%M, %Y")

    # Extract month and day from departing_LEX for arriving_NOR
    date_part_lex = departing_LEX.strftime("%B %d, %Y")  # Extracts "March 25, 2025"
    arriving_NOR_time_only = arriving_NOR_time[i].strip()
    arriving_NOR_str = f"{date_part_lex}, {arriving_NOR_time_only}"
    arriving_NOR = datetime.strptime(arriving_NOR_str, "%B %d, %Y, %H:%M")

    # Adjust for overnight flights (if arrival is earlier than departure, it must be the next day)
    if arriving_LEX < departing_NOR:
        arriving_LEX += timedelta(days=1)
    if arriving_NOR < departing_LEX:
        arriving_NOR += timedelta(days=1)

    # Check if departing from Norfolk before 5PM Friday
    if departing_NOR.strftime("%A") == "Friday" and departing_NOR.hour < 17:
        days_off += 1

    # Check the arrival day back in Norfolk with Corrected Year
    arriving_nor_day = arriving_NOR.strftime("%A")
    if arriving_nor_day == "Monday":
        days_off += 1
    elif arriving_nor_day == "Tuesday":
        days_off += 2

    # Store the days off for each flight
    days_off_list.append(days_off)

# If you want to see all the results at once:
print("Days Off Needed: ", days_off_list)


# Fourth, we want to print out the 8 cheapest flights and the days off needed for each flight
# We will sort the flights by price and print out the top 8
# We will also print out the days off needed for each flight

# Combine the flight details into a list of tuples
flight_details = list(zip(carrier, departing_NOR_time, arriving_LEX_time, departing_LEX_time, arriving_NOR_time, price, total_price, days_off_list))

# Sort the flights by total price
flight_details.sort(key=lambda x: x[6])

# Print the 8 cheapest flights and the days off needed for each flight
print("\n8 Cheapest Flights:")
for i in range(8):
    print(f"Flight {i+1}:")
    print(f"Carrier: {flight_details[i][0]}")
    print(f"Departing Norfolk: {flight_details[i][1]}")
    print(f"Arriving Lexington: {flight_details[i][2]}")
    print(f"Departing Lexington: {flight_details[i][3]}")
    print(f"Arriving Norfolk: {flight_details[i][4]}")
    print(f"Ticket Price: ${flight_details[i][5]}")
    print(f"Total Price: ${flight_details[i][6]}")
    print(f"Days Off Needed: {flight_details[i][7]}")
    print()

