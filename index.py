import customtkinter as cus
root = cus.CTk()
root.geometry("1800x769")
root.title("Register")


name_label = cus.CTkLabel(root, text="Name")
name_label.grid(row=0, column=0, padx=100, pady=7)
position_label = cus.CTkLabel(root, text="Position")
position_label.grid(row=0, column=1, padx=100, pady=7)
date_label = cus.CTkLabel(root, text="Date")
date_label.grid(row=0, column=2, padx=100, pady=7)
time_label = cus.CTkLabel(root, text="Time")
time_label.grid(row=0, column=3, padx=100, pady=7)
Total_label = cus.CTkLabel(root, text="Total work days")
Total_label.grid(row=0, column=4, padx=100, pady=7)

 
frame = cus.CTkFrame(root,fg_color="#2a2a2a")
frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=20, pady=(0, 20))
frame_label = cus.CTkFrame(frame,fg_color="#ada3a3",height=60)
frame_label.grid(row=0, column=0, columnspan=10, sticky="ew", padx=10, pady= 10)
frame.grid_propagate(False)

for i in range(5):
    frame.grid_columnconfigure(i,weight=1)

for i in range(5):
    root.grid_columnconfigure(i, weight=1)
root.grid_rowconfigure(1, weight=1)  

root.mainloop()