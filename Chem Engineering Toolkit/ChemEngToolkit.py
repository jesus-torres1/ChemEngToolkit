"""
Chemical Engineering Toolkit

This program provides two calculators:
1. Liquid Spill Volume Calculator: Calculates the volume of a liquid spill based on user input.
2. Gas Release Rate Calculator: Estimates gas flow rates based on user input.

"""

__Author__ = """ Jesus Torres """

import math
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Constants for unit conversions
ATM_PRESSURE_PSI = 14.696  # Atmospheric pressure in psi
CUBIC_METER_TO_CUBIC_FEET = 35.3147  # Conversion factor from cubic meters to cubic feet

# Function to format the volume with both cubic feet and gallons
def format_volume(volume):
    cubic_feet = volume
    gallons = volume * 7.48052  # 1 cubic foot = 7.48052 gallons
    return f"{cubic_feet:.2f} cubic feet ({gallons:.2f} gallons)"

# Function to calculate and display the liquid spill volume
def calculate_volume():
    shape = shape_var.get()
    
    if shape == "Rectangular":
        length_str = length_entry.get()
        width_str = width_entry.get()
        depth_str = depth_entry.get()
        
        if not length_str or not width_str or not depth_str:
            messagebox.showerror("Input Error", "Please enter all dimensions.")
            return
        
        length = float(length_str)
        width = float(width_str)
        depth = float(depth_str)
        
        volume = length * width * depth
    elif shape == "Circular":
        length_str = length_entry.get()
        depth_str = depth_entry.get()
        
        if not length_str or not depth_str:
            messagebox.showerror("Input Error", "Please enter both length and depth.")
            return
        
        length = float(length_str)
        depth = float(depth_str)
        radius = length / 2
        
        volume = math.pi * (radius**2) * depth
    else:
        messagebox.showerror("Input Error", "Please select a shape.")
        return
    
    formatted_volume = format_volume(volume)
    result_label.config(text=f"Volume: {formatted_volume}")

    # Clear input fields
    length_entry.delete(0, tk.END)
    width_entry.delete(0, tk.END)
    depth_entry.delete(0, tk.END)

# Function to calculate flow rate
def calculate_flow_rate(diameter, source_pressure, gas_temperature, discharge_coefficient):
    # Convert source pressure to pascals
    source_pressure_pa = source_pressure * 6894.76  # psi to Pa
    
    # Calculate gas density using the ideal gas law
    GAS_CONSTANT = 8.314  # J/(mol·K)
    gas_density = source_pressure_pa / (GAS_CONSTANT * gas_temperature)
    
    # Calculate flow rate in cubic meters per second
    flow_rate_m3_s = discharge_coefficient * math.pi * ((diameter/2)**2) * math.sqrt(2 * (source_pressure_pa - ATM_PRESSURE_PSI*6894.76) / gas_density)
    
    # Convert flow rate to cubic feet per second
    flow_rate_ft3_s = flow_rate_m3_s * CUBIC_METER_TO_CUBIC_FEET
    
    return flow_rate_m3_s, flow_rate_ft3_s

# Function to calculate gas release rate
def calculate_gas_release_rate():
    try:
        diameter = float(diameter_entry.get())
        source_pressure = float(source_pressure_entry.get())
        gas_temperature = float(gas_temperature_entry.get())
        discharge_coefficient = float(discharge_coefficient_entry.get())
        
        # Calculate gas release rate using the provided formula
        flow_rate_m3_s, flow_rate_ft3_s = calculate_flow_rate(diameter, source_pressure, gas_temperature, discharge_coefficient)
        
        result_gas_label.config(text=f"Flow Rate (m³/s): {flow_rate_m3_s:.2f}\nFlow Rate (ft³/s): {flow_rate_ft3_s:.2f}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# Create the main GUI window
root = tk.Tk()
root.title("Chemical Engineering Toolkit - Author: Jesus Torres")

# Create a frame for the Liquid Spill Volume Calculator (left side)
frame_left = tk.Frame(root, bg="#ffffff")
frame_left.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

# Load and display the logo for the Liquid Spill Volume Calculator
liquid_spill_logo = Image.open("spill.png")  # Replace with the path to your logo image
liquid_spill_logo = liquid_spill_logo.resize((150, 150), Image.ANTIALIAS)  # Resize the logo as needed
liquid_spill_logo_photo = ImageTk.PhotoImage(liquid_spill_logo)
liquid_spill_logo_label = tk.Label(frame_left, image=liquid_spill_logo_photo, bg="#ffffff")
liquid_spill_logo_label.photo = liquid_spill_logo_photo
liquid_spill_logo_label.grid(row=0, column=0, columnspan=2, pady=10)

# Liquid Spill Volume Calculator title
title_label_left = tk.Label(frame_left, text="Liquid Spill Volume Calculator", font=("Arial", 16), bg="#ffffff")
title_label_left.grid(row=1, column=0, columnspan=2, pady=10)

shape_var = tk.StringVar()
shape_var.set("Rectangular")

shape_label = tk.Label(frame_left, text="Select Shape:", font=("Arial", 12), bg="#ffffff")
shape_label.grid(row=2, column=0, columnspan=2, sticky="w")

shape_radios = [
    tk.Radiobutton(frame_left, text="Rectangular", variable=shape_var, value="Rectangular", font=("Arial", 10)),
    tk.Radiobutton(frame_left, text="Circular", variable=shape_var, value="Circular", font=("Arial", 10))
]

shape_radios[0].grid(row=3, column=0, columnspan=2, sticky="w")
shape_radios[1].grid(row=4, column=0, columnspan=2, sticky="w")

frame2_left = tk.Frame(frame_left, bg="#ffffff")
frame2_left.grid(row=5, column=0, columnspan=2, pady=10)

length_label = tk.Label(frame2_left, text="Length (feet):", font=("Arial", 12), bg="#ffffff")
length_label.grid(row=0, column=0, sticky="e")
length_entry = tk.Entry(frame2_left)
length_entry.grid(row=0, column=1)

width_label = tk.Label(frame2_left, text="Width (feet):", font=("Arial", 12), bg="#ffffff")
width_label.grid(row=1, column=0, sticky="e")
width_entry = tk.Entry(frame2_left)
width_entry.grid(row=1, column=1)

depth_label = tk.Label(frame2_left, text="Depth (feet):", font=("Arial", 12), bg="#ffffff")
depth_label.grid(row=2, column=0, sticky="e")
depth_entry = tk.Entry(frame2_left)
depth_entry.grid(row=2, column=1)

calculate_button = tk.Button(frame2_left, text="Calculate", command=calculate_volume, font=("Arial", 12))
calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

result_label = tk.Label(frame2_left, text="", font=("Arial", 12), bg="#ffffff")
result_label.grid(row=4, column=0, columnspan=2)

# Create a frame for the Gas Release Rate Calculator (right side)
frame_right = tk.Frame(root, bg="#ffffff")
frame_right.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

# Load and display the logo for the Gas Release Rate Calculator
gas_release_logo = Image.open("burner.png")  # Replace with the path to your logo image
gas_release_logo = gas_release_logo.resize((150, 150), Image.ANTIALIAS)  # Resize the logo as needed
gas_release_logo_photo = ImageTk.PhotoImage(gas_release_logo)
gas_release_logo_label = tk.Label(frame_right, image=gas_release_logo_photo, bg="#ffffff")
gas_release_logo_label.photo = gas_release_logo_photo
gas_release_logo_label.grid(row=0, column=0, columnspan=2, pady=10)

# Gas Release Rate Calculator title
title_label_right = tk.Label(frame_right, text="Gas Release Rate Calculator", font=("Arial", 16), bg="#ffffff")
title_label_right.grid(row=1, column=0, columnspan=2, pady=10)

# Labels and entry fields for user input
diameter_label = tk.Label(frame_right, text="Orifice Diameter (inches):", font=("Arial", 12), bg="#ffffff")
diameter_label.grid(row=2, column=0, sticky="e")
diameter_entry = tk.Entry(frame_right)
diameter_entry.grid(row=2, column=1)

source_pressure_label = tk.Label(frame_right, text="Source Pressure (psi):", font=("Arial", 12), bg="#ffffff")
source_pressure_label.grid(row=3, column=0, sticky="e")
source_pressure_entry = tk.Entry(frame_right)
source_pressure_entry.grid(row=3, column=1)

gas_temperature_label = tk.Label(frame_right, text="Gas Temperature (Kelvin):", font=("Arial", 12), bg="#ffffff")
gas_temperature_label.grid(row=4, column=0, sticky="e")
gas_temperature_entry = tk.Entry(frame_right)
gas_temperature_entry.grid(row=4, column=1)

discharge_coefficient_label = tk.Label(frame_right, text="Discharge Coefficient:", font=("Arial", 12), bg="#ffffff")
discharge_coefficient_label.grid(row=5, column=0, sticky="e")
discharge_coefficient_entry = tk.Entry(frame_right)
discharge_coefficient_entry.grid(row=5, column=1)

# Button to calculate gas release rate
calculate_gas_button = tk.Button(frame_right, text="Calculate", command=calculate_gas_release_rate, font=("Arial", 12))
calculate_gas_button.grid(row=6, column=0, columnspan=2, pady=10)

# Label to display the result
result_gas_label = tk.Label(frame_right, text="", font=("Arial", 12), bg="#ffffff")
result_gas_label.grid(row=7, column=0, columnspan=2)

# Note (moved to the lower right bottom)
disclaimer_text = "Note: Gas flow rate calculations are for quick estimation. For accurate gas flow rate calculations, consult engineering references.\n" \
                  "Spilled Bucket Image by brgfx on Freepik\n" \
                  "Bunsen Burner image by OpenClipart-Vector from Pixabay"

disclaimer_label = tk.Label(frame_right, text=disclaimer_text, font=("Arial", 10), bg="#ffffff", anchor="e")
disclaimer_label.grid(row=8, column=0, columnspan=2, pady=(0, 10), sticky="se")


# Configure the grid layout
frame_left.grid_rowconfigure(0, weight=1)
frame_left.grid_columnconfigure(0, weight=1)
frame_right.grid_rowconfigure(0, weight=1)
frame_right.grid_columnconfigure(0, weight=1)
frame_right.grid_columnconfigure(1, weight=1)

# Start the GUI main loop
root.mainloop()
