import customtkinter as cus
from datetime import datetime
import mysql.connector

today = datetime.now().date()
current_time = datetime.now().strftime("%I:%M %p")

root = cus.CTk()
root.geometry("1800x769")
root.title("Register")

# Header Frame (Fixed at the top)
header_frame = cus.CTkFrame(root, fg_color="#99C57C")
header_frame.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=20, pady=(10, 0))

headers = ["Name", "Position", "Date", "Time", "Total"]
for idx, text in enumerate(headers):
    label = cus.CTkLabel(header_frame, text=text, font=("Arial", 14, "bold"), text_color="white")
    label.grid(row=0, column=idx, padx=10, pady=7, sticky="nsew")
    header_frame.grid_columnconfigure(idx, weight=1)

# Scrollable Frame for data
frame = cus.CTkScrollableFrame(root, fg_color="#2a2a2a", width=1700, height=650)
frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=20, pady=(0, 20))

for i in range(len(headers)):
    frame.grid_columnconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)
root.grid_rowconfigure(1, weight=1)

record_row = 0

def add_employee(name, position):
    global record_row
    display_row = record_row + 1
    cus.CTkLabel(frame, text=name).grid(row=display_row, column=0, padx=10, pady=7, sticky="nsew")
    cus.CTkLabel(frame, text=position).grid(row=display_row, column=1, padx=10, pady=7, sticky="nsew")
    cus.CTkLabel(frame, text=today).grid(row=display_row, column=2, padx=8, pady=7, sticky="nsew")
    cus.CTkLabel(frame, text=current_time).grid(row=display_row, column=3, padx=7, pady=7, sticky="nsew")
    cus.CTkLabel(frame, text="0").grid(row=display_row, column=4, padx=6, pady=7, sticky="nsew")
    record_row += 1

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
        password = password_entry.get()
        work_date = datetime.now().date()
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

            add_employee(name, position)
            popup.destroy()
        except mysql.connector.Error as err:
            print("Error:", err)

    submit_button = cus.CTkButton(popup, text="Submit", command=submit_data)
    submit_button.pack(pady=10)

button = cus.CTkButton(root, text="Add Employee", command=pop_up)
button.grid(row=2, column=0, padx=10, pady=10)

def mark_employee():
    popup = cus.CTkToplevel(root)
    popup.geometry("400x250")
    popup.title("Mark Attendance")

    name_entry = cus.CTkEntry(popup, placeholder_text="Name")
    name_entry.pack(pady=10)

    password_entry = cus.CTkEntry(popup, placeholder_text="Password")
    password_entry.pack(pady=10)

    message_label = cus.CTkLabel(popup, text="")
    message_label.pack(pady=10)

    def check_employee():
        name = name_entry.get()
        password = password_entry.get()

        if not name or not password:
            message_label.configure(text="Please enter both fields", text_color="red")
            return

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="MyStr0ngP@ssw0rd",
                database="farm_db"
            )
            cursor = connection.cursor()

            cursor.execute("SELECT total_days_worked FROM employees WHERE name=%s AND password=%s", (name, password))
            results = cursor.fetchall()

            if results:
                total_days = results[0][0] + 1
                now = datetime.now()
                cursor.execute("""
                    UPDATE employees
                    SET total_days_worked = %s, work_date = %s, work_time = %s
                    WHERE name = %s AND password = %s
                """, (total_days, now.date(), now.time().strftime("%H:%M:%S"), name, password))
                connection.commit()
                message_label.configure(text="Attendance Marked!", text_color="green")
            else:
                message_label.configure(text="Invalid name or password", text_color="red")

            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            message_label.configure(text=f"Error: {err}", text_color="red")

    check = cus.CTkButton(popup, text="Check", command=check_employee)
    check.pack(pady=10)

mark_button = cus.CTkButton(root, text="Mark", command=mark_employee)
mark_button.grid(row=2, column=1, padx=10, pady=10)

# Load all employees on startup
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="MyStr0ngP@ssw0rd",
        database="farm_db"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT name, position, work_date, work_time, total_days_worked FROM employees")
    records = cursor.fetchall()
    record_row = 0
    for row_index, row_data in enumerate(records, start=1):
        for col_index, value in enumerate(row_data):
            cus.CTkLabel(frame, text=value).grid(row=row_index, column=col_index, padx=10, pady=7, sticky="nsew")
        record_row += 1
    cursor.close()
    connection.close()
except mysql.connector.Error as err:
    print("Error loading data:", err)

root.mainloop()
