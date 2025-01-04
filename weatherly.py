import requests
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import datetime

# OpenWeatherMap API Key
API_KEY = "your_api_key_here"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Toggle unit for temperature (Celsius/Fahrenheit)
temp_unit = "metric"

# Function to fetch weather data
def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city name!")
        return

    try:
        params = {"q": city, "appid": API_KEY, "units": temp_unit}
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data["cod"] != 200:
            messagebox.showerror("Error", data.get("message", "City not found. Please try again."))
            return

        # Extract weather data
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        description = data["weather"][0]["description"].title()
        icon_code = data["weather"][0]["icon"]

        # Convert timestamp to readable time
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).strftime('%H:%M:%S')
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"]).strftime('%H:%M:%S')

        # Update GUI elements
        temp_label.config(text=f"Temperature: {temp}°{'C' if temp_unit == 'metric' else 'F'}")
        desc_label.config(text=f"Description: {description}")
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_label.config(text=f"Wind Speed: {wind_speed} m/s")
        sunrise_label.config(text=f"Sunrise: {sunrise}")
        sunset_label.config(text=f"Sunset: {sunset}")

        # Fetch and display weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url, stream=True)
        if icon_response.status_code == 200:
            img_data = icon_response.raw.read()
            icon_image = ImageTk.PhotoImage(Image.open(io.BytesIO(img_data)))
            icon_label.config(image=icon_image)
            icon_label.image = icon_image

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Toggle temperature unit
def toggle_unit():
    global temp_unit
    temp_unit = "metric" if temp_unit == "imperial" else "imperial"
    unit_button.config(text="Switch to °F" if temp_unit == "imperial" else "Switch to °C")

# Tkinter GUI setup
root = tk.Tk()
root.title("Weatherly 🌤️ - Advanced Weather App")
root.geometry("500x500")
root.resizable(False, False)

# Title
title_label = tk.Label(root, text="Weatherly 🌤️", font=("Helvetica", 18, "bold"))
title_label.pack(pady=10)

# Input and search
city_label = tk.Label(root, text="Enter City Name:", font=("Helvetica", 12))
city_label.pack(pady=5)

city_entry = tk.Entry(root, font=("Helvetica", 12), width=30)
city_entry.pack(pady=5)

search_button = tk.Button(root, text="Get Weather", font=("Helvetica", 12), command=get_weather)
search_button.pack(pady=10)

# Weather details
icon_label = tk.Label(root)
icon_label.pack(pady=10)

temp_label = tk.Label(root, text="", font=("Helvetica", 12))
temp_label.pack()

desc_label = tk.Label(root, text="", font=("Helvetica", 12))
desc_label.pack()

humidity_label = tk.Label(root, text="", font=("Helvetica", 12))
humidity_label.pack()

wind_label = tk.Label(root, text="", font=("Helvetica", 12))
wind_label.pack()

sunrise_label = tk.Label(root, text="", font=("Helvetica", 12))
sunrise_label.pack()

sunset_label = tk.Label(root, text="", font=("Helvetica", 12))
sunset_label.pack()

# Toggle unit button
unit_button = tk.Button(root, text="Switch to °F", font=("Helvetica", 12), command=toggle_unit)
unit_button.pack(pady=10)

# Run the application
root.mainloop()
