import customtkinter as cus
from datetime import datetime
import mysql.connector 


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
header_frame = cus.CTkFrame(frame, fg_color="#7EC44F")
header_frame.grid(row=0, column=0,columnspan=5, sticky="nsew")
headers = ["Name", "Position", "Date", "Time", "Total work days"]
for idx, text in enumerate(headers):
    cus.CTkLabel(header_frame, text=text, font=("Arial", 14, "bold"), text_color="white").grid(
        row=0, column=idx, padx=10, pady=7, sticky="nsew"
    )
    header_frame.grid_columnconfigure(idx, weight=1)


for i in range(5):
    frame.grid_columnconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)
root.grid_rowconfigure(1, weight=1)

# Row tracker for employee records
record_row = 0


def add_employee(name, position):
    global record_row
    display_row = record_row + 1  # Start below the header frame
    cus.CTkLabel(frame, text=name).grid(row=display_row, column=0, padx=10, pady=7, sticky="nsew")
    cus.CTkLabel(frame, text=position).grid(row=display_row, column=1, padx=10, pady=7, sticky="nsew")
    cus.CTkLabel(frame, text=today).grid(row=display_row, column=2, padx=8, pady=7, sticky="nsew")
    cus.CTkLabel(frame, text=current_time).grid(row=display_row, column=3, padx=7, pady=7, sticky="nsew")
    cus.CTkLabel(frame, text="0").grid(row=display_row, column=4, padx=6, pady=7, sticky="nsew")
    record_row += 1


# add_employee("John", "Regular")


def pop_up():
    popup = cus.CTkToplevel(root)
    popup.geometry("400x200")
    popup.title("Add Employee")

    name_entry = cus.CTkEntry(popup, placeholder_text="Name")
    name_entry.pack(pady=10)
    position_entry = cus.CTkEntry(popup, placeholder_text="Position")
    position_entry.pack(pady=10)
    password_entry = cus.CTkEntry(popup, placeholder_text="Password")
    password_entry.pack(pady=10)

    def submit_data():
        name = name_entry.get()
        position = position_entry.get()
        password= password_entry.get()
        work_date=datetime.now().date()
        work_time = datetime.now().time().strftime("%H:%M:%S")
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="MyStr0ngP@ssw0rd",
                database="farm_db"
            )
            cursor = conn.cursor()
            query = """
                INSERT INTO employees (name, position, work_date, work_time, total_days_worked, password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (name, position, work_date, work_time, 1, password)
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()

            add_employee(name, position)  # Add to GUI
            popup.destroy()
        except mysql.connector.Error as err:
            print("Error:", err)  # You can replace this with a CTk messagebox if needed

    submit_button = cus.CTkButton(popup, text="Submit", command=submit_data)
    submit_button.pack(pady=10)

# Add button
button = cus.CTkButton(root, text="Add Employee", command=pop_up)
button.grid(row=2, column=0, padx=10, pady=10)


root.mainloop()
