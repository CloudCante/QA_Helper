import os
import customtkinter as ctk
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkcalendar import DateEntry  # Importing the DateEntry widget
from PIL import Image, ImageTk  # To work with images

def rename_file(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        messagebox.showinfo("Success", f'Renamed "{old_name}" to "{new_name}"')
    except Exception as e:
        messagebox.showerror("Error", str(e))

def drop(event):
    file_path = event.data.strip()  # Normalize the file path
    print(f"Dropped file path: '{file_path}'")  # Debugging output

    file_path = file_path.strip('{}').replace("\\", "/")  # Clean up the file path

    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            batch_number = batch_entry.get()
            if not batch_number:
                messagebox.showerror("Error", "Batch number must be provided.")
                return

            # Get values from the dropdowns and calendar
            date = date_entry.get()  # Get the date from the calendar
            part_name = part_name_var.get()
            side = side_var.get()
            type_ = type_var.get()
            test_name = test_var.get()

            _, ext = os.path.splitext(file_path)

            # Create the new name, retaining the original file extension
            new_name = f"{date} {part_name} {side} {type_} Batch {batch_number} {test_name}{ext}"
            print(f"New name: '{new_name}'")  # Debugging output

            new_full_path = os.path.join(os.path.dirname(file_path), new_name)
            print(f"New full path: '{new_full_path}'")  # Debugging output

            rename_file(file_path, new_full_path)
        else:
            messagebox.showerror("Error", "Dropped item is not a valid file.")
    else:
        messagebox.showerror("Error", f"The file does not exist: {file_path}")

# Set up the main application window using CustomTkinter
ctk.set_appearance_mode("System")  # Set light/dark mode automatically based on system preference
ctk.set_default_color_theme("blue")  # You can change the theme (e.g., "dark-blue", "green", "light")

root = TkinterDnD.Tk()
root.title("File Renamer")
root.geometry("600x400")

# Load the background image
bg_image = Image.open("bg_for_helper.jpg")  # Ensure this file is in the same folder
bg_image = bg_image.resize((600, 400), Image.Resampling.LANCZOS)  # Resize the image to match the window size
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a canvas widget to hold the background image
canvas = ctk.CTkCanvas(root, width=600, height=400)
canvas.pack(fill="both", expand=True)

# Place the background image on the canvas
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# Create the main frame using CustomTkinter inside the canvas
main_frame = ctk.CTkFrame(canvas, fg_color="transparent")  # Make the background transparent
main_frame.place(relwidth=1, relheight=1)  # Ensure it takes up the full space of the canvas

# Grid layout setup
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_rowconfigure(2, weight=1)
main_frame.grid_rowconfigure(3, weight=1)
main_frame.grid_rowconfigure(4, weight=1)
main_frame.grid_rowconfigure(5, weight=1)
main_frame.grid_rowconfigure(6, weight=1)
main_frame.grid_rowconfigure(7, weight=2)  # Making row 7 (drag and drop) more responsive

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)  # Column 1 will take more space

# Calendar for Date Selection
date_label = ctk.CTkLabel(main_frame, text="Select Date:")
date_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
date_entry = DateEntry(main_frame, date_pattern='mm-dd-yyyy')
date_entry.grid(row=0, column=1, padx=1, pady=1, sticky="w")

# Dropdown for Part Name
part_name_var = ctk.StringVar(root)
part_name_options = ["Ford Bronco", "Ford Ranger", "Ford Redback", "Toyota 200D", "Toyota 910B", "Audi MLBw", "Audi A294", "Audi A296", "910B"]
part_name_var.set(part_name_options[0])  # Default value
part_name_menu = ctk.CTkOptionMenu(main_frame, variable=part_name_var, values=part_name_options)
part_name_menu.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Dropdown for Type
type_var = ctk.StringVar(root)
type_options = ["WC", "SK", "CA"]
type_var.set(type_options[0])  # Default value
type_menu = ctk.CTkOptionMenu(main_frame, variable=type_var, values=type_options)
type_menu.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Dropdown for Side
side_var = ctk.StringVar(root)
side_options = ["LH", "RH"]
side_var.set(side_options[0])  # Default value
side_menu = ctk.CTkOptionMenu(main_frame, variable=side_var, values=side_options)
side_menu.grid(row=3, column=1, padx=10, pady=5, sticky="w")

# Dropdown for Test Name
test_var = ctk.StringVar(root)
test_options = ["Micros"]  # Add test options here
test_var.set(test_options[0])  # Default value
test_menu = ctk.CTkOptionMenu(main_frame, variable=test_var, values=test_options)
test_menu.grid(row=4, column=1, padx=10, pady=5, sticky="w")

# Entry for Lab Number
lab_number_label = ctk.CTkLabel(main_frame, text="Lab Number:")
lab_number_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
lab_number_entry = ctk.CTkEntry(main_frame)
lab_number_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

# Entry for Batch Number
batch_label = ctk.CTkLabel(main_frame, text="Batch Number:")
batch_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
batch_entry = ctk.CTkEntry(main_frame)
batch_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")

# Label for drag and drop - span across both columns (0 and 1) and center it
label = ctk.CTkLabel(main_frame, text="Drag and drop a file here", pady=50)
label.grid(row=7, column=0, columnspan=2, padx=10, pady=20, sticky="ew")  # Spans both columns

# Center the label content horizontally within the expanded space
label.configure(anchor="center")

# Set up drag-and-drop functionality
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

root.mainloop()







