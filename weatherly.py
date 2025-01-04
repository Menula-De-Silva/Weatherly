import requests
import tkinter as tk
from tkinter import messagebox

# OpenWeatherMap API Key (Replace with your API key)
API_KEY = "your_api_key_here"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Function to get weather details
def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name!")
        return

    # Make a request to OpenWeatherMap API
    try:
        params = {"q": city, "appid": API_KEY, "units": "metric"}
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data["cod"] != 200:
            messagebox.showerror("Error", data.get("message", "Unable to fetch weather data."))
            return

        # Extracting and displaying weather data
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        description = data["weather"][0]["description"]

        weather_info = f"City: {city}\nTemperature: {temp}°C\nHumidity: {humidity}%\nWind Speed: {wind_speed} m/s\nDescription: {description.title()}"
        weather_label.config(text=weather_info)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Tkinter GUI Setup
root = tk.Tk()
root.title("Weatherly 🌤️")
root.geometry("400x300")
root.resizable(False, False)

# GUI Widgets
title_label = tk.Label(root, text="Weatherly 🌤️", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

city_label = tk.Label(root, text="Enter City Name:", font=("Helvetica", 12))
city_label.pack(pady=5)

city_entry = tk.Entry(root, font=("Helvetica", 12), width=25)
city_entry.pack(pady=5)

search_button = tk.Button(root, text="Get Weather", font=("Helvetica", 12), command=get_weather)
search_button.pack(pady=10)

weather_label = tk.Label(root, text="", font=("Helvetica", 12), justify="left", wraplength=350)
weather_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
