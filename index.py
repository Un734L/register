import customtkinter as cus
from datetime import datetime


today = datetime.now().date()
current_time = datetime.now().strftime("%I:%M %p")


root = cus.CTk()
root.geometry("1800x769")
root.title("Register")

# # Headers (placed in the same frame as employee rows)
# headers = ["Name", "Position", "Date", "Time", "Total work days"]
# for idx, text in enumerate(headers):
#     cus.CTkLabel(root, text=text, font=("Arial", 16, "bold")).grid(row=0, column=idx, padx=10, pady=10)


frame = cus.CTkFrame(root, fg_color="#2a2a2a")
frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=20, pady=(0, 20))
frame.grid_propagate(False)
# Place headers inside the frame (row 0)
headers = ["Name", "Position", "Date", "Time", "Total work days"]
for idx, text in enumerate(headers):
    cus.CTkLabel(frame, text=text, font=("Arial", 14, "bold")).grid(row=0, column=idx, padx=10, pady=10, sticky="nsew")


for i in range(5):
    frame.grid_columnconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)
root.grid_rowconfigure(1, weight=1)

# Row tracker for employee records
record_row = 0


def add_employee(name, position):
    global record_row
    display_row = record_row + 1  # shift down by 1 to leave space for header row
    cus.CTkLabel(frame, text=name).grid(row=display_row, column=0)
    cus.CTkLabel(frame, text=position).grid(row=display_row, column=1)
    cus.CTkLabel(frame, text=today).grid(row=display_row, column=2)
    cus.CTkLabel(frame, text=current_time).grid(row=display_row, column=3)
    cus.CTkLabel(frame, text="0").grid(row=display_row, column=4)
    record_row += 1


add_employee("John", "Regular")


def pop_up():
    popup = cus.CTkToplevel(root)
    popup.geometry("400x200")
    popup.title("Add Employee")

    name_entry = cus.CTkEntry(popup, placeholder_text="Name")
    name_entry.pack(pady=10)
    position_entry = cus.CTkEntry(popup, placeholder_text="Position")
    position_entry.pack(pady=10)

    def submit_fun():
        name = name_entry.get()
        position = position_entry.get()
        if name and position:
            add_employee(name, position)
            popup.destroy()  
        else:
            print("Please enter both name and position.")

    submit_button = cus.CTkButton(popup, text="Submit", command=submit_fun)
    submit_button.pack(pady=10)

# Add button
button = cus.CTkButton(root, text="Add Employee", command=pop_up)
button.grid(row=2, column=0, padx=10, pady=10)


root.mainloop()
