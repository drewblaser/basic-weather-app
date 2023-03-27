from tkinter import *
from tkinter import messagebox
import requests
from dotenv import load_dotenv
import os


def configure():
    load_dotenv()


def get_weather(city):
    configure()
    city = city_entry.get()
    params = {"q": city,
    "appid": os.getenv("OWM_API_KEY")
    }
    weather = requests.get(url="https://api.openweathermap.org/data/2.5/weather", params=params)
    if weather:
        data = weather.json()
        city = data["name"]
        country = data["sys"]["country"]
        description = data["weather"][0]["description"]
        temp_kelvin = data["main"]["temp"]
        temp_f = round((temp_kelvin-273.15) * 9/5+32)
        icon_file = data["weather"][0]["icon"]
        final = (description, temp_f, icon_file, city, country)
        return final


def search():
    city = city_entry.get()
    weather = get_weather(city)

    if weather:
        temp.config(text=f"{weather[1]} °F", font=("Verb", 30, "bold"))
        global icon
        icon = PhotoImage(file=f"icons/{weather[2]}.png")
        canvas.itemconfig(image_id, image=icon)
        w_description.config(text=f"{weather[0]}", font=("Verb", 15, "bold"))
        location.config(text=f"{weather[3]}, {weather[4]}", font=("Verb", 12,), pady=10)
    elif city_entry.get() == "":
        messagebox.showerror(title="Error", message=f"Please Enter a city.")
    else:
        messagebox.showerror(title="Error", message=f"Cannot find data for {city}")


window = Tk()
window.config(pady=20, padx=20, bg="dark cyan")
window.title("Weather App")
window.minsize(300, 300)

w_description = Label(bg="dark cyan", fg="white")
w_description.pack()

canvas = Canvas(window, width=100, height=100, highlightthickness=0, bg="dark cyan")
canvas.pack()
icon = PhotoImage()
image_id = canvas.create_image(50, 50, image=icon,)

location = Label(bg="dark cyan", fg="white")
location.pack()

temp = Label(bg="dark cyan", fg="white")
temp.pack()

city_entry = Entry()
city_entry.pack(pady=10)

search_button = Button(text="Search", command=search)
search_button.pack()


window.mainloop()