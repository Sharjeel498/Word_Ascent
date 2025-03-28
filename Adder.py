import tkinter as tk
import re
import csv
import os

class Adder:
    # Validation function that checks if the input is a string (only letters)
    def validate_input(self, char):
        return re.match('^[a-zA-ZäöüßÄÖÜòàùèé ]+$', char) is not None
    
    # Constructor for Adder
    def __init__(self, root, start_frame):
        self.root = root
        validate_command = root.register(self.validate_input)
        font = ("Times", 25)
        self.meaning_array = []

        # Word label and entry
        self.add_frame = tk.Frame(root, bg="lightblue")
        tk.Label(self.add_frame, text= "Word", font= font, bg="lightblue").grid(row= 1, column= 0, padx= 10, pady= 10)
        self.word_entry = tk.Entry(self.add_frame, font= font, width=25,validate= 'all', validatecommand=(validate_command, '%S'))
        self.word_entry.grid(row = 1, column= 1, padx= 10, pady= 10)

        # Meaning label and entry
        tk.Label(self.add_frame, text= "Meaning", font= font, bg="lightblue").grid(row= 2, column= 0, padx= 10, pady= 10)
        self.meaning_entry = tk.Entry(self.add_frame, font= font, width= 25,validate= 'all', validatecommand=(validate_command,'%S'))
        self.meaning_entry.grid(row = 2, column= 1, padx= 10, pady= 10)

        # Buttons 
        self.add_meaning_btn = tk.Button(self.add_frame, text = "+", font = font, width = 2, command = lambda: self.append_meaning())
        self.add_meaning_btn.grid(row = 2, column=2,  padx= 10, pady= 10)
        
        self.add_button = tk.Button(self.add_frame, text = "Add", font= font, width= 7,command= lambda: self.add())
        self.add_button.grid(row = 4, column=1,  padx= 10, pady= 10)
        tk.Button(self.add_frame, text = "Back", font= font, width= 7,command= lambda: self.go_back(start_frame)).grid(row = 4, column=0,  padx= 10, pady= 10)
        
        self.warning = tk.Label(self.add_frame, text = "The word already contains 5 meanings i.e. the maximum allowed.", font = ("Times", 18), bg = "lightblue", width= 30, wraplength=200)
        self.warning.grid(row = 5, column= 0, columnspan=3, rowspan=2, padx = 10, pady = 10)
        self.warning.grid_remove()

        self.add_frame.pack(fill="both", expand=True)
        self.word_entry.focus_set()

        # Bind Enter key in first entry to move focus to second entry
        self.word_entry.bind('<Return>', lambda event: self.meaning_entry.focus_set())

        # Bind Enter key in second entry to trigger the button
        self.meaning_entry.bind('<Return>', lambda event: self.add())

    # Method to handle multiple meanings for a word
    def append_meaning(self):
        entry = self.meaning_entry.get()
        new_meaning = False
        if len(self.meaning_array) == 0:
            added, append_level = self.check_word_exists()
        if len(self.meaning_array) < 5:
            if (entry not in self.meaning_array):
                if len(entry) > 1:
                    self.meaning_array.append(entry)
                    self.meaning_entry.delete(0, tk.END)
                    new_meaning = True                   # variable indicating that a new meaning has to be added for the word.
            else:
                self.meaning_entry.delete(0, tk.END)
        else:                                           # Limiting the number of meanings to 5
            self.add_meaning_btn.config(bg = "red")
            self.add_frame.after(500, lambda: self.add_meaning_btn.configure(bg = "SystemButtonFace"))
            self.warning.grid()
            self.add_frame.after(5000, lambda: self.warning.grid_remove())
            self.add(added, append_level, new_meaning)

    def restore_button_color(self, og_color):
        if self.add_button.winfo_exists():
            self.add_button.configure(bg=og_color)

    def check_word_exists(self):
        added = False # word not present in the dictionary
        # Check if the word pair is already present in any of the layers.
        for i in range(1, 6):
            with open(f"Level_{i}.csv", "r+", newline="", encoding="latin-1") as reading_file:
                reader = csv.reader(reading_file)
                has_rows = any(reader)  # Check if there's at least one row
                if has_rows:
                    for row in reader:
                        if self.word_entry.get() == row[0]:
                            added = True
                            existing_meanings = row[1:]
                            if 'nan' in existing_meanings:
                                existing_meanings.remove('nan')
                            self.meaning_array = existing_meanings
                            return [added, i]
        return [added, 0]
                            
    # Method to add a word pair to Level_1.csv
    def add(self, added= None, append_level= None, new_meaning = None):
        self.word = self.word_entry.get()
        og_color = "SystemButtonFace"
        entry = self.meaning_entry.get()

        print(self.word)  
        if len(self.word) > 0:
            if added is None:
                added, append_level = self.check_word_exists()
                if len(self.meaning_array) < 5:
                    if len(entry) > 1 and (entry not in self.meaning_array):
                        self.meaning_array.append(entry)
                        new_meaning = True
                        self.meaning_entry.delete(0, tk.END)
                else:
                    self.add_button.config(bg = "red")
                    self.add_frame.after(500, lambda: self.restore_button_color(og_color))
                    self.warning.grid()
                    self.add_frame.after(5000, lambda: self.warning.grid_remove())

            if new_meaning:
                print("new meaning")
                if added:
                    file = f"Level_{append_level}.csv"
                    temp_file = f"Level_{append_level}.tmp"
                    with open(file, "r+", newline="", encoding="latin-1") as infile, \
                        open(temp_file, "a+", newline="", encoding="latin-1") as outfile:
                            reader_2 = csv.reader(infile)
                            writer = csv.writer(outfile)
                            writer.writerows(row for row in reader_2 if row[0] != self.word)  # Fast filtering
                            writer.writerow([self.word] + self.meaning_array) 
                    
                    os.replace(temp_file, file)
                    self.add_button.config(bg = "green") # indicates word addition.
                    self.add_frame.after(500, lambda: self.restore_button_color(og_color))

                else:
                    with open(f"Level_1.csv", "a", newline="", encoding="latin-1") as level_1:
                        writer = csv.writer(level_1)
                        writer.writerow([self.word] + self.meaning_array)
                        
                    self.add_button.config(bg = "green") 
                    self.add_frame.after(500, lambda: self.restore_button_color(og_color))

        self.word_entry.delete(0, tk.END)
        self.meaning_entry.delete(0, tk.END)
        self.meaning_array = []
        self.to_append = False
        self.word_entry.focus_set()

    # Method to go back to initial Interface class GUI.
    def go_back(self, start_frame):
        self.add_frame.pack_forget()
        start_frame.pack(fill = "both", expand= True)
        del self
