import tkinter as tk
import requests
from datetime import datetime

def weather_icon(desc):
    desc = desc.lower()
    if "sun" in desc:
        return "☀️"
    if "cloud" in desc:
        return "☁️"
    if "rain" in desc:
        return "🌧️"
    if "storm" in desc:
        return "⛈️"
    return "🌤️"

def save_history(city):
    with open("weather_history.txt", "a") as file:
        file.write(city + " - " + datetime.now().strftime("%Y-%m-%d %H:%M") + "\n")

def get_weather():
    city = city_entry.get().strip()

    if city == "":
        output.config(text="Please enter a city name")
        return

    try:
        url = f"https://wttr.in/{city}?format=j1"
        data = requests.get(url).json()

        current = data["current_condition"][0]
        forecast = data["weather"]

        text = f"📍 {city.upper()}\n\n"
        text += f"{weather_icon(current['weatherDesc'][0]['value'])}  "
        text += f"{current['weatherDesc'][0]['value']}\n"
        text += f"🌡️ Temp: {current['temp_C']} °C\n"
        text += f"💧 Humidity: {current['humidity']}%\n"
        text += f"💨 Wind: {current['windspeedKmph']} km/h\n\n"

        text += "📅 Forecast:\n"

        for day in forecast[:3]:
            date = day["date"]
            avg = day["avgtempC"]
            desc = day["hourly"][4]["weatherDesc"][0]["value"]
            text += f"{date}: {avg} °C {weather_icon(desc)}\n"

        output.config(text=text)
        save_history(city)

    except:
        output.config(text="City not found or no internet")

# ---------- GUI ----------
root = tk.Tk()
root.title("Advanced Weather App v2")
root.geometry("420x500")
root.configure(bg="#121212")

tk.Label(
    root,
    text="Advanced Weather App",
    font=("Arial", 18, "bold"),
    bg="#121212",
    fg="cyan"
).pack(pady=10)

city_entry = tk.Entry(root, font=("Arial", 14), justify="center")
city_entry.pack(pady=10)

tk.Button(
    root,
    text="Get Weather",
    font=("Arial", 12),
    command=get_weather,
    bg="cyan",
    fg="black"
).pack(pady=10)

output = tk.Label(
    root,
    text="",
    font=("Arial", 12),
    bg="#121212",
    fg="white",
    justify="left"
)
output.pack(pady=20)

root.mainloop()
