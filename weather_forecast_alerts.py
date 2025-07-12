import requests
import pandas as pd

API_KEY = "90c0dfb905532c01642befc9b9cc0308"

BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

cities = ["London", "New York", "Delhi", "Tokyo"]

# List to hold all weather alerts
weather_alerts = []

# Process each city
for city in cities:
    print(f"\nFetching forecast for {city}...")

    # Construct request URL
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"

    try:
        # Send API request
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()

        if "list" not in data:
            print(f"No forecast data available for {city}.")
            continue

        forecast_entries = data["list"]
        processed_data = []

        for entry in forecast_entries:
            date = entry["dt_txt"]
            temp = entry["main"]["temp"]
            humidity = entry["main"]["humidity"]
            condition = entry["weather"][0]["main"].lower()

            # Add to structured data
            processed_data.append({
                "Date": date,
                "Temperature": temp,
                "Humidity": humidity,
                "Condition": condition.capitalize()
            })

            # Generate alerts
            if temp > 35:
                weather_alerts.append(f"High Temperature Alert in {city} on {date}")
            elif temp < 5:
                weather_alerts.append(f"Cold Weather Alert in {city} on {date}")
            if "rain" in condition or "storm" in condition:
                weather_alerts.append(f"Storm/Rain Alert in {city} on {date}")

        # Save to CSV file
        df = pd.DataFrame(processed_data)
        file_name = f"{city.replace(' ', '_')}_forecast.csv"
        df.to_csv(file_name, index=False)
        print(f"Forecast saved to {file_name}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error for {city}: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error for {city}: {req_err}")
    except Exception as err:
        print(f"Unexpected error for {city}: {err}")

# Save all alerts to a text file
if weather_alerts:
    with open("weather_alerts.txt", "w") as f:
        for alert in weather_alerts:
            f.write(alert + "\n")
    print("Weather alerts saved to weather_alerts.txt")
else:
    print("No extreme weather alerts generated.")