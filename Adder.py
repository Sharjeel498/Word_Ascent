import tkinter as tk
import re
import csv

class Adder:
    # Validation function that checks if the input is a string (only letters)
    def validate_input(self, char):
        return re.match('^[a-zA-ZäöüßÄÖÜ ]+$', char) is not None
    
    # Constructor for Adder
    def __init__(self, root, start_frame):
        self.root = root
        validate_command = root.register(self.validate_input)

        font = ("Times", 25)

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
        tk.Button(self.add_frame, text = "Add", font= font, width= 7,command= lambda: self.add()).grid(row = 3, column=1,  padx= 10, pady= 10)
        tk.Button(self.add_frame, text = "Back", font= font, width= 7,command= lambda: self.go_back(start_frame)).grid(row = 3, column=0,  padx= 10, pady= 10)

        self.add_frame.pack(fill="both", expand=True)
    
    # Method to add a word pair to Level_1.csv
    def add(self):
        self.word = self.word_entry.get()
        self.meaning = self.meaning_entry.get()
        
        if len(self.word) > 0 and len(self.meaning) > 0:
            with open("Level_1.csv", "a+", newline= "", encoding="latin-1") as level_1:
                writer = csv.writer(level_1)
                added = False # word already present in the dictionary
                
                # Check if the word pair is already present in any of the layers.
                for i in range(1, 6):
                    with open(f"Level_{i}.csv", "r+", newline="", encoding="latin-1") as file:
                        reader = csv.reader(file)
                        for row in reader:
                            if [self.word, self.meaning] == row:
                                added = True
                                break

                if added == False:
                    writer.writerow([self.word, self.meaning])

            self.word_entry.delete(0, tk.END)
            self.meaning_entry.delete(0, tk.END)

    # Method to go back to initial Interface class GUI.
    def go_back(self, start_frame):
        self.add_frame.pack_forget()
        start_frame.pack(fill = "both", expand= True)
        del self
