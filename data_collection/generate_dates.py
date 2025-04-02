from datetime import datetime, timedelta

# Define start and end dates
start_date = datetime(1940, 1, 1)
end_date = datetime(2025, 3, 15)

# Generate list of 1st of each month
dates = []
current = start_date.replace(day=1)
while current <= end_date:
    dates.append(current)
    fifteenth = current.replace(day=15)
    if fifteenth <= end_date and current.day != 15:
        dates.append(fifteenth)
    if current.month == 12:
        current = current.replace(year=current.year + 1, month=1)
    else:
        current = current.replace(month=current.month + 1)

# Format as required (YYYY-MM-DDT00:00:00Z)
date_strings = [date.strftime("%Y-%m-%dT00:00:00Z")[:10] for date in dates]

print(date_strings)

# Save to a text file
with open("../data/date_windows.txt", "w") as f:
    for date in date_strings:
        f.write(date + "\n")

print("✅ Date windows saved to 'date_windows.txt'!")