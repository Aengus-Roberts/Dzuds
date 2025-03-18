from datetime import datetime, timedelta

# Define start and end dates
start_date = datetime(2016, 1, 1)
end_date = datetime(2025, 3, 15)

# Define the interval (e.g., every 10 days)
interval_days = 5

# Generate date list
dates = [start_date + timedelta(days=i) for i in range(0, (end_date - start_date).days + 1, interval_days)]

# Format as required (YYYY-MM-DDT00:00:00Z)
date_strings = [date.strftime("%Y-%m-%dT00:00:00Z") for date in dates]

# Save to a text file
with open("date_windows.txt", "w") as f:
    for date in date_strings:
        f.write(date + "\n")

print("✅ Date windows saved to 'date_windows.txt'!")