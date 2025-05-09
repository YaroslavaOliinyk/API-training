import requests
from datetime import datetime

API_KEY = 'DEMO_KEY'  
API_URL = 'https://api.nasa.gov/neo/rest/v1/feed'

def get_neo_data(start_date, end_date):
    """Fetch Near Earth Object data from NASA API."""
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'api_key': API_KEY
    }
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def display_asteroids(data):
    """Display asteroid data in a readable format."""
    if not data:
        print("No data to display.")
        return

    neos = data.get('near_earth_objects', {})
    for date in sorted(neos.keys()):
        print(f"\nDate: {date}")
        for asteroid in neos[date]:
            name = asteroid.get('name', 'Unknown')
            diameter = asteroid.get('estimated_diameter', {}).get('meters', {})
            size = f"{int(diameter.get('min', 0))} - {int(diameter.get('max', 0))} m"
            velocity = asteroid.get('close_approach_data', [{}])[0].get('relative_velocity', {}).get('kilometers_per_hour', '0')
            distance = asteroid.get('close_approach_data', [{}])[0].get('miss_distance', {}).get('kilometers', '0')
            hazardous = asteroid.get('is_potentially_hazardous_asteroid', False)

            print(f" - {name}")
            print(f"    Size: {size}")
            print(f"    Velocity: {float(velocity):,.0f} km/h")
            print(f"    Distance from Earth: {float(distance):,.0f} km")
            print(f"    Potentially Hazardous: {'Yes' if hazardous else 'No'}\n")

def validate_date(date_str):
    """Validate date format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    print("NASA Near Earth Object Tracker")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    # Date validation
    if not validate_date(start_date) or not validate_date(end_date):
        print("Invalid date format. Please use YYYY-MM-DD.")
        exit()

    data = get_neo_data(start_date, end_date)
    display_asteroids(data)