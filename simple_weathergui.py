import requests
import json
import datetime
import tkinter as tk
from tkinter.ttk import *
import weather_codes
import os
from PIL import Image, ImageTk

class SimpleWeatherGUI(tk.Tk):
        def __init__(self):
                super().__init__()
                self.location=tk.StringVar()
                self.locat_entry=tk.Entry(self, textvariable=self.location,font=("Times New Roman", 20))
                self.locat_entry.pack(padx=10, pady=5)
                self.submit_button=tk.Button(self, text="Show weather",font=("Times New Roman", 14), command=self.start_process)
                self.submit_button.pack(padx=10, pady=10)               
                self.images=[]
                self.bind("<Return>", self.start_process)
                self.mainloop()
        
        def get_weather_data(self):
                address=self.location.get()
                geocode=requests.get(f"https://geocode.maps.co/search?q={address}&api_key=680bff74e339c625259862jui43355b")
                geo_content=geocode.json()[0]
                lat=float(geo_content["lat"])
                lon=float(geo_content["lon"])
                fields={"weatherCodeMax": "Condition",
                        "temperatureAvg": "Temperature",                       
                        "pressureSeaLevelAvg": "Pressure",
                        "humidityAvg": "Humidity",
                        "windSpeedAvg": "Wind Speed"}
                units_list=[None,"°C", "hPa","%", "m/s"]
                units="metric"
                response=requests.get(f"https://api.tomorrow.io/v4/weather/forecast?", params={"location": f"{lat}, {lon}", "apikey":"vVC7meoSDArLWyTgJMU2XA9v2o0VbKlI", "fields": ",".join(list(fields.keys())), "units": units, "timesteps": "1d"})
                data=response.json()
 
                self.setup_ui(address)
                for x in range(2, 8):  
                        self.parent_treeview(data["timelines"]["daily"][x-2]["time"], x)       
                for y in range(6):
                        self.child_treeview(y, fields, data["timelines"]["daily"][y]["values"], units_list)        

        def setup_ui(self, address):
                self.scroll_tree_frame=tk.Frame(self)
                self.scroll_tree_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
                self.weekdays={0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5:"Saturday", 6: "Sunday"}                
                self.my_treeview=Treeview(self.scroll_tree_frame, selectmode="browse")
                self.my_treeview.grid(row=0, column=0, sticky="nsew")
                my_scrollb_y=Scrollbar(self.scroll_tree_frame, orient="vertical", command=self.my_treeview.yview)
                my_scrollb_y.grid(row=0, column=1, sticky="ns")
                self.my_treeview.configure(yscrollcommand=my_scrollb_y.set)
                self.scroll_tree_frame.grid_rowconfigure(0, weight=1)
                self.scroll_tree_frame.grid_columnconfigure(0, weight=1)
                self.my_treeview.heading("#0", text="Weather GUI")
                self.my_treeview.insert("", 0, "item1", text=f"Weather in {address}")

        def parent_treeview(self,time,x):        
                dt=datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
                weekday=dt.weekday()
                self.my_treeview.insert("item1", x-1, "item"+str(x), text=self.weekdays[weekday])

        def child_treeview(self, y, fields, day_values, units_list):      
                y+=2         
                for f, h in fields.items():
                        if f!="weatherCodeMax":
                                self.my_treeview.insert("item"+str(y), "end", f"{f} {y-1}", text=f"{h}: {day_values[f]} {units_list[list(fields.keys()).index(f)]}")
                        else:
                                weather_path=os.path.join(weather_codes.base_path, weather_codes.weatherCode[day_values[f]])
                                img=Image.open(weather_path)
                                img=img.resize((20, 20))
                                img_tk=ImageTk.PhotoImage(img)
                                self.images.append(img_tk)
                                self.my_treeview.insert("item"+str(y), "end", f"{h} {y-1}",text=f" {weather_codes.weatherCodeText[day_values[f]]} " , image=img_tk) 

        def start_process(self, *args):
                try:
                     self.scroll_tree_frame.destroy()
                except:
                        None              
                self.get_weather_data()                                                       

start=SimpleWeatherGUI()

"""requirements
1. Entry (location)
2. Button "Search wetter"
3. Treeview
Postal code, Location name, country
pressure, humidity, speed
today&tomorrow: detailed hourly
7 days: temp, condition

toggle switch Celcius/Fahrenheit
icon comdition
bg?
print(json.dumps(data,indent=2))
"""