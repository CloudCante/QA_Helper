import customtkinter as ctk
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkcalendar import DateEntry
from object_detect_label import load_and_label_pdf, rename_file  # Import functions from the other module

class FileProcessorApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        # Set up the appearance and window settings
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.root.title("QA Helper")
        self.root.geometry("600x400")

        # Create the main frame
        main_frame = ctk.CTkFrame(self.root, fg_color="white")
        main_frame.pack(fill="both", expand=True)

        # Set up grid layout for UI components (restoring the original 7 rows and 2 columns)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_rowconfigure(4, weight=1)
        main_frame.grid_rowconfigure(5, weight=1)
        main_frame.grid_rowconfigure(6, weight=1)
        main_frame.grid_rowconfigure(7, weight=2)  # Making row 7 more responsive

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # Calendar for Date Selection
        date_label = ctk.CTkLabel(main_frame, text="Select Date:")
        date_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.date_entry = DateEntry(main_frame, date_pattern='mm-dd-yyyy')
        self.date_entry.grid(row=0, column=1, padx=1, pady=1, sticky="w")

        # Dropdown for Part Name
        self.part_name_var = ctk.StringVar(self.root)
        part_name_options = ["Ford Bronco", "Ford Ranger", "Ford Redback", "Toyota 200D", "Toyota 910B", "Audi MLBw", "Audi A294", "Audi A296", "Toyota 910B"]  # Part names
        self.part_name_var.set(part_name_options[0])  # Default value
        part_name_menu = ctk.CTkOptionMenu(main_frame, variable=self.part_name_var, values=part_name_options)
        part_name_menu.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Entry for Lab Number
        lab_number_label = ctk.CTkLabel(main_frame, text="Lab Number:")
        lab_number_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.lab_number_entry = ctk.CTkEntry(main_frame)
        self.lab_number_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Dropdown for Type
        type_var = ctk.StringVar(self.root)
        type_options = ["WC", "SK", "CA"]  # Original options
        type_var.set(type_options[0])  # Default value
        type_menu = ctk.CTkOptionMenu(main_frame, variable=type_var, values=type_options)
        type_menu.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Dropdown for Side
        side_var = ctk.StringVar(self.root)
        side_options = ["LH", "RH"]  # Original options
        side_var.set(side_options[0])  # Default value
        side_menu = ctk.CTkOptionMenu(main_frame, variable=side_var, values=side_options)
        side_menu.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Dropdown for Test Name
        test_var = ctk.StringVar(self.root)
        test_options = ["Micros"]  # Original test options
        test_var.set(test_options[0])  # Default value
        test_menu = ctk.CTkOptionMenu(main_frame, variable=test_var, values=test_options)
        test_menu.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Entry for Batch Number
        batch_label = ctk.CTkLabel(main_frame, text="Batch Number:")
        batch_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.batch_entry = ctk.CTkEntry(main_frame)
        self.batch_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        # Label for drag and drop - span across both columns (0 and 1) and center it
        label = ctk.CTkLabel(main_frame, text="Drag and drop a file here", pady=50)
        label.grid(row=7, column=0, columnspan=2, padx=10, pady=20, sticky="ew")  # Spans both columns
        label.configure(anchor="center")

        # Set up drag-and-drop functionality
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)

    def on_drop(self, event):
        # Step 1: Handle the dropped file
        pdf_path = event.data.strip('{}').replace("\\", "/")  # Get file path from dropped file
        print(f"Dropped file path: '{pdf_path}'")

        # Step 2: Get user inputs
        date = self.date_entry.get()
        part_name = self.part_name_var.get()
        lab_number = self.lab_number_entry.get()
        batch_number = self.batch_entry.get()

        if not batch_number or not lab_number:
            messagebox.showerror("Error", "Batch number and Lab number must be provided.")
            return

        # Step 3: Call functions from `object_detect_label.py` to process the file
        labeled_pdf_path = load_and_label_pdf(pdf_path, part_name, lab_number)  # Label the file

        # Step 4: Rename the labeled file using user inputs
        new_name = f"{date} {part_name} Batch {batch_number}.pdf"
        rename_file(labeled_pdf_path, new_name)

        # Inform the user that the process was successful
        messagebox.showinfo("Success", f"File processed and saved as: {new_name}")

# Running the app
if __name__ == "__main__":
    root = TkinterDnD.Tk()  # Use TkinterDnD for drag-and-drop support
    app = FileProcessorApp(root)
    root.mainloop()















