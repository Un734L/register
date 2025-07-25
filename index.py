import customtkinter as cus
from datetime import datetime
import mysql.connector
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

today = datetime.now().date()
current_time = datetime.now().strftime("%I:%M %p")

root = cus.CTk()
root.geometry("1800x769")
root.title("Register")

# Header Frame
header_frame = cus.CTkFrame(root, fg_color="#226079")
header_frame.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=20, pady=(10, 0))

headers = ["Name", "Position", "Date", "Time", "Total"]
for idx, text in enumerate(headers):
    label = cus.CTkLabel(header_frame, text=text, font=("Arial", 14, "bold"), text_color="white")
    label.grid(row=0, column=idx, padx=10, pady=7, sticky="nsew")
    header_frame.grid_columnconfigure(idx, weight=1)

# Scrollable Frame
frame = cus.CTkScrollableFrame(root, fg_color="#2a2a2a", width=1700, height=650)
frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=20, pady=(0, 20))

for i in range(len(headers)):
    frame.grid_columnconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)
root.grid_rowconfigure(1, weight=1)

# Clear and Reload Employee Records
def load_employees():
    for widget in frame.winfo_children():
        widget.destroy()

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MyStr0ngP@ssw0rd",
            database="farm_db"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT name, position, work_date, work_time, total_days_worked FROM employees")
        records = cursor.fetchall()
        for row_index, row_data in enumerate(records, start=1):
            for col_index, value in enumerate(row_data):
                cus.CTkLabel(frame, text=value).grid(row=row_index, column=col_index, padx=10, pady=7, sticky="nsew")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("Error loading data:", err)

# Add Employee Popup
def pop_up():
    popup = cus.CTkToplevel(root)
    popup.geometry("400x300")
    popup.title("Add Employee")

    name_entry = cus.CTkEntry(popup, placeholder_text="Name")
    name_entry.pack(pady=10)
    position_entry = cus.CTkEntry(popup, placeholder_text="Position")
    position_entry.pack(pady=10)
    wage_entry = cus.CTkEntry(popup, placeholder_text="wage per day (K)")
    wage_entry.pack(pady=10)
    password_entry = cus.CTkEntry(popup, placeholder_text="Password",show="*")
    password_entry.pack(pady=10)

    def submit_data():
        name = name_entry.get()
        position = position_entry.get()
        wage = wage_entry.get()  
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
                INSERT INTO employees (name, position, work_date, work_time, total_days_worked, password, wage)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (name, position, work_date, work_time, 1, password, wage)
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()

            popup.destroy()
            load_employees()
        except mysql.connector.Error as err:
            print("Error:", err)

    submit_button = cus.CTkButton(popup, text="Submit", command=submit_data)
    submit_button.pack(pady=10)

# Mark Attendance Popup
def mark_employee():
    popup = cus.CTkToplevel(root)
    popup.geometry("400x250")
    popup.title("Mark Attendance")

    name_entry = cus.CTkEntry(popup, placeholder_text="Name")
    name_entry.pack(pady=10)

    password_entry = cus.CTkEntry(popup, placeholder_text="Password",show="*")
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
                load_employees()
            else:
                message_label.configure(text="Invalid name or password", text_color="red")

            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            message_label.configure(text=f"Error: {err}", text_color="red")

    check = cus.CTkButton(popup, text="Check", command=check_employee)
    check.pack(pady=10)

# Download PDF
def download_pdf():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="MyStr0ngP@ssw0rd",
        database="farm_db"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT name, wage, total_days_worked FROM employees")
    results = cursor.fetchall()

    pdf_file = "employee_report.pdf"
    c = canvas.Canvas(pdf_file, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, y, "Employee Wage Report")
    y -= 40

    c.setFont("Helvetica", 12)

    for row in results:
        name, wage, days_worked = row
        try:
            total_pay = float(wage) * int(days_worked)
        except:
            total_pay = 0

        c.drawString(50, y, str(name))
        y -= 15
        c.drawString(50, y, f"Total Wage: K{total_pay:.2f}")
        y -= 30  # Space between entries

        if y < 60:
            c.showPage()
            y = height - 50

    c.save()

    popup = cus.CTkToplevel(root)
    popup.geometry("300x100")
    popup.title("PDF")
    cus.CTkLabel(popup, text=f"PDF saved as {pdf_file}", text_color="green").pack(pady=20)
    cus.CTkButton(popup, text="Close", command=popup.destroy).pack(pady=10)
# Buttons
cus.CTkButton(root, text="Add Employee", command=pop_up).grid(row=2, column=0, padx=10, pady=10)
cus.CTkButton(root, text="Mark", command=mark_employee).grid(row=2, column=1, padx=10, pady=10)

def delete_employee():
    popup = cus.CTkToplevel(root)
    popup.geometry("400x200")
    popup.title("Delete Employee")

    name_entry = cus.CTkEntry(popup, placeholder_text="Name")
    name_entry.pack(pady=10)
    password_entry = cus.CTkEntry(popup, placeholder_text="Password",show="*")
    password_entry.pack(pady=10)

    def delete_data():
        name = name_entry.get()
        password = password_entry.get()
        if not name or not password:
            cus.CTkLabel(popup, text="Please enter a name", text_color="red").pack(pady=10)
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="MyStr0ngP@ssw0rd",
                database="farm_db"
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employees WHERE name=%s AND password = %s", (name, password))
            conn.commit()
            cursor.close()
            conn.close()

            popup.destroy()
            load_employees()
        except mysql.connector.Error as err:
            cus.CTkLabel(popup, text=f"Error: {err}", text_color="red").pack(pady=10)

    delete_button = cus.CTkButton(popup, text="Delete", command=delete_data)
    delete_button.pack(pady=10)

cus.CTkButton(root, text="Delete Employee", command=delete_employee).grid(row=2, column=2, padx=10, pady=10)


cus.CTkButton(root, text="Download PDF", command=download_pdf).grid(row=2, column=3, padx=10, pady=10)

# Initial Load
load_employees()
root.mainloop()
