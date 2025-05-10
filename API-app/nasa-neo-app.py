import requests
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext

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
        return {"error": f"Error fetching data: {e}"}

def validate_date(date_str):
    """Validate date format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def fetch_data():
    """Fetch data and display it in the GUI."""
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()

    # Validate dates
    if not validate_date(start_date) or not validate_date(end_date):
        messagebox.showerror("Invalid Input", "Invalid date format. Use YYYY-MM-DD.")
        return

    # Fetch data
    data = get_neo_data(start_date, end_date)
    if "error" in data:
        messagebox.showerror("Error", data["error"])
        return

    # Display data
    neos = data.get('near_earth_objects', {})
    result_text.delete(1.0, tk.END)  # Clear previous results
    for date in sorted(neos.keys()):
        result_text.insert(tk.END, f"\nDate: {date}\n")
        for asteroid in neos[date]:
            name = asteroid.get('name', 'Unknown')
            diameter = asteroid.get('estimated_diameter', {}).get('meters', {})
            min_diameter = diameter.get('estimated_diameter_min', 0)
            max_diameter = diameter.get('estimated_diameter_max', 0)
            size = f"{int(min_diameter)} - {int(max_diameter)} m"
            velocity = asteroid.get('close_approach_data', [{}])[0].get('relative_velocity', {}).get('kilometers_per_hour', '0')
            distance = asteroid.get('close_approach_data', [{}])[0].get('miss_distance', {}).get('kilometers', '0')
            hazardous = asteroid.get('is_potentially_hazardous_asteroid', False)

            result_text.insert(tk.END, f" - {name}\n")
            result_text.insert(tk.END, f"    Size: {size}\n")
            result_text.insert(tk.END, f"    Velocity: {float(velocity):,.0f} km/h\n")
            result_text.insert(tk.END, f"    Distance from Earth: {float(distance):,.0f} km\n")
            result_text.insert(tk.END, f"    Potentially Hazardous: {'Yes' if hazardous else 'No'}\n\n")

# Create the GUI
root = tk.Tk()
root.title("NASA Near Earth Object Tracker")

# Input fields
tk.Label(root, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
start_date_entry = tk.Entry(root, width=20)
start_date_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
end_date_entry = tk.Entry(root, width=20)
end_date_entry.grid(row=1, column=1, padx=10, pady=5)

# Fetch button
fetch_button = tk.Button(root, text="Fetch Data", command=fetch_data)
fetch_button.grid(row=2, column=0, columnspan=2, pady=10)

# Result display
result_text = scrolledtext.ScrolledText(root, width=80, height=20)
result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Run the GUI
root.mainloop()

