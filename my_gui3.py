import tkinter as tk
from tkinter import messagebox

class PatientDataEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Patient Data Editor")
        self.master.geometry("800x400")  # Increase the width of the window

        self.patient_data = []
        self.edit_mode = False
        self.selected_index = None

        self.setup_gui()

    def setup_gui(self):
        # Labels and Entry Widgets for Patient Information
        self.label_name = tk.Label(self.master, text="Name:")
        self.entry_name = tk.Entry(self.master)

        self.label_age = tk.Label(self.master, text="Age:")
        self.entry_age = tk.Entry(self.master)

        self.label_gender = tk.Label(self.master, text="Gender:")
        self.entry_gender = tk.Entry(self.master)

        self.label_phone = tk.Label(self.master, text="Phone:")
        self.entry_phone = tk.Entry(self.master)

        self.label_aadhar = tk.Label(self.master, text="Aadhar:")
        self.entry_aadhar = tk.Entry(self.master)

        # Buttons for Adding, Editing, and Updating Patient Data
        self.add_button = tk.Button(self.master, text="Add Patient", command=self.add_patient)
        self.edit_button = tk.Button(self.master, text="Edit Patient", command=self.enable_edit_mode, state=tk.DISABLED)
        self.update_button = tk.Button(self.master, text="Update", command=self.update_patient, state=tk.DISABLED)

        # Listbox to Display Patient Data
        self.patient_listbox = tk.Listbox(self.master, selectmode=tk.SINGLE, width=40, height=10)
        self.patient_listbox.bind("<Double-Button-1>", self.enable_edit_mode)
        self.patient_listbox.bind("<<ListboxSelect>>", self.toggle_buttons_state)

        # Place widgets on the grid
        self.label_name.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        self.label_age.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_age.grid(row=1, column=1, padx=10, pady=5)

        self.label_gender.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_gender.grid(row=2, column=1, padx=10, pady=5)

        self.label_phone.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_phone.grid(row=3, column=1, padx=10, pady=5)

        self.label_aadhar.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.entry_aadhar.grid(row=4, column=1, padx=10, pady=5)

        self.add_button.grid(row=5, column=0, pady=10, padx=10, sticky="w")  # Adjust button position
        self.edit_button.grid(row=5, column=1, pady=10, padx=10, sticky="w")  # Adjust button position
        self.update_button.grid(row=5, column=2, pady=10, padx=10, sticky="w")  # Adjust button position

        self.patient_listbox.grid(row=0, column=3, rowspan=6, padx=10, pady=10, sticky="nsew", columnspan=2)  # Increase columnspan

    def add_patient(self):
        name = self.entry_name.get()
        age = self.entry_age.get()
        gender = self.entry_gender.get()
        phone = self.entry_phone.get()
        aadhar = self.entry_aadhar.get()

        if name and age.isdigit() and phone.isdigit() and aadhar.isdigit() and self.is_aadhar_valid(aadhar) and self.is_phone_valid(phone) and self.is_aadhar_unique(aadhar):
            patient_info = f"Name: {name}, Age: {age}, Gender: {gender}, Phone: {phone}, Aadhar: {aadhar}"
            self.patient_data.append(patient_info)
            self.update_patient_listbox()
            self.clear_entry_fields()
        else:
            messagebox.showwarning("Invalid Information", "Please enter valid and unique patient details.")

    def enable_edit_mode(self, event=None):
        selected_index = self.patient_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            patient_info = self.patient_data[selected_index].split(", ")
            self.populate_entry_fields(patient_info)
            self.edit_mode = True
            self.selected_index = selected_index
            self.toggle_buttons_state()

    def update_patient(self):
        if self.edit_mode and self.selected_index is not None:
            edited_info = self.get_patient_info_from_entries()
            if self.is_valid_patient_info(edited_info, self.selected_index):
                self.patient_data[self.selected_index] = edited_info
                self.update_patient_listbox()
                self.clear_entry_fields()
                self.disable_edit_mode()
            else:
                messagebox.showwarning("Invalid Information", "Please enter valid and unique patient details.")

    def is_valid_patient_info(self, patient_info, current_index):
        name, age, gender, phone, aadhar = self.get_patient_info_values(patient_info)

        if not age.isdigit():
            messagebox.showwarning("Invalid Information", "Age must be numerical.")
            return False

        if not phone.isdigit() or not self.is_phone_valid(phone):
            messagebox.showwarning("Invalid Information", "Enter a 10-digit phone number.")
            return False

        if not aadhar.isdigit() or not self.is_aadhar_valid(aadhar):
            messagebox.showwarning("Invalid Information", "Enter a 12-digit Aadhar number.")
            return False

        if not self.is_aadhar_unique(aadhar, current_index):
            return False

        return True

    def is_aadhar_valid(self, aadhar):
        return len(aadhar) == 12

    def is_phone_valid(self, phone):
        return len(phone) == 10

    def is_aadhar_unique(self, aadhar, current_index=None):
        for i, patient_info in enumerate(self.patient_data):
            if i == current_index:
                continue
            _, _, _, _, existing_aadhar = self.get_patient_info_values(patient_info)
            if aadhar == existing_aadhar:
                return False
        return True

    def get_patient_info_values(self, patient_info):
        items = [item.split(": ") for item in patient_info.split(", ")]
        name, age, gender, phone, aadhar = [value for _, value in items]
        return name, age, gender, phone, aadhar

    def toggle_buttons_state(self, event=None):
        if self.patient_listbox.curselection() and not self.edit_mode:
            self.edit_button["state"] = tk.NORMAL
            self.update_button["state"] = tk.DISABLED
        elif self.edit_mode:
            self.edit_button["state"] = tk.DISABLED
            self.update_button["state"] = tk.NORMAL
        else:
            self.edit_button["state"] = tk.DISABLED
            self.update_button["state"] = tk.DISABLED

    def update_patient_listbox(self):
        self.patient_listbox.delete(0, tk.END)
        for patient_info in self.patient_data:
            self.patient_listbox.insert(tk.END, patient_info)

    def clear_entry_fields(self):
        self.entry_name.delete(0, tk.END)
        self.entry_age.delete(0, tk.END)
        self.entry_gender.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.entry_aadhar.delete(0, tk.END)

    def get_patient_info_from_entries(self):
        name = self.entry_name.get()
        age = self.entry_age.get()
        gender = self.entry_gender.get()
        phone = self.entry_phone.get()
        aadhar = self.entry_aadhar.get()
        return f"Name: {name}, Age: {age}, Gender: {gender}, Phone: {phone}, Aadhar: {aadhar}"

    def populate_entry_fields(self, patient_info):
        self.clear_entry_fields()
        for item in patient_info:
            key, value = item.split(": ")
            if key == "Name":
                self.entry_name.insert(0, value)
            elif key == "Age":
                self.entry_age.insert(0, value)
            elif key == "Gender":
                self.entry_gender.insert(0, value)
            elif key == "Phone":
                self.entry_phone.insert(0, value)
            elif key == "Aadhar":
                self.entry_aadhar.insert(0, value)

    def disable_edit_mode(self):
        self.edit_mode = False
        self.selected_index = None
        self.toggle_buttons_state()

def main():
    root = tk.Tk()
    app = PatientDataEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
