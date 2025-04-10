import tkinter as tk
import re
import pandas as pd
import random
import os
import csv
import warnings

class Tester:

    # Function to get word and a meaning from one of the levels
    def get_word(self):
        level = random.randint(1, 5)
        self.level = level

        # Iterates over all levels to get a word pair if Level_{level}.csv is empty.
        i = 1
        while i <= 6: # i goes from 1 to 6 because level is always i-1 after the first iteration.
            try:
                self.df = pd.read_csv(f"Level_{level}.csv", encoding= 'latin-1')
                if len(self.df) > 0:
                    break
            except Exception as e:
                print(e)

            # Level_{level}.csv was empty, so now we try Level_{level+1}.csv
            level = i
            self.level = level
            i += 1

        num_rows = len(self.df)

        if self.level >= 5 and num_rows == 0: # There are no words in any of the levels
            return False
    
        meaning_column_names = [f"meaning_{i}" for i in range(1, self.df.shape[1])]
        self.df.columns = ["word"] + meaning_column_names

        if num_rows > 1:   # if the level has more than one pair
            random_index = random.randint(0, num_rows - 1)
        else:
            random_index = 0

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.pair = self.df.iloc[random_index]
            self.word = self.pair[0]
            self.meaning = self.pair[1:].dropna().tolist()


    # This method restricts user input to only allowed characters such as alphabets
    def validate_input(self, char):
        return re.match('^[a-zA-ZäöüßÄÖÜòàùèé ]+$', char) is not None

    # Constructor for Tester   
    def __init__(self, root, start_frame):
        self.start_frame = start_frame
        self.root = root
        validate_command = root.register(self.validate_input)
        word_exists = self.get_word()

        self.test_frame = tk.Frame(root, bg="lightblue")
        font = ("Times", 25)
        self.font = font

        # If dictionary is empty
        if word_exists == False:
            print("There are no words in the files")
            tk.Label(self.test_frame, text= "All levels are empty. Please add words.", font= self.font,).grid(row= 2, column= 1, padx= 10, pady= 10)
            tk.Button(self.test_frame, text = "Back", font= font, width= 7,command= lambda: self.go_back(start_frame)).grid(row = 3, column=1,  padx= 10, pady= 10)
            self.test_frame.pack(fill= "both", expand=True)
            return

        # Word Labels
        tk.Label(self.test_frame, text= "Word --> ", font= font, bg="lightblue").grid(row= 1, column= 0, padx= 10, pady= 10)
        self.word_label = tk.Label(self.test_frame, text= f"{self.word}", font= font, bg="lightblue")
        self.word_label.grid(row= 1, column= 1, padx= 10, pady= 10)

        # Meaning Label and entry
        tk.Label(self.test_frame, text= "Meaning --> ", font= font, bg="lightblue").grid(row= 2, column= 0, padx= 10, pady= 10)
        self.meaning_entry = tk.Entry(self.test_frame, font= font, width= 20, validate= 'all', validatecommand=(validate_command,'%S'))
        self.meaning_entry.grid(row = 2, column= 1, padx= 10, pady= 10)
        self.meaning_entry.focus_set()
        self.meaning_entry.bind('<Return>', lambda event: self.check())

        # Check button for entry
        self.check_btn = tk.Button(self.test_frame, text= "Check", font= font, width= 7, command= self.check)
        self.check_btn.grid(row = 3, column= 1, padx= 10, pady= 10)
        tk.Button(self.test_frame, text = "Back", font= font, width= 7,command= lambda: self.go_back(start_frame)).grid(row = 3, column=0,  padx= 10, pady= 10)

        self.give_up_btn = tk.Button(self.test_frame, text = "Give up", font = font, width= 7, command = lambda: self.give_up())
        self.give_up_btn.grid(row = 4, column= 0, padx = 10, pady = 10)
        self.give_up_btn.grid_remove()


        self.meaning_label = tk.Label(self.test_frame, text = " ", font = font, bg = "lightblue", width= 20, wraplength=200)
        self.meaning_label.grid(row = 4, column= 1, columnspan=2, rowspan=2, padx = 10, pady = 10)
        self.meaning_label.grid_remove()

        self.test_frame.pack(fill= "both", expand=True)

    def restore_button_color(self, og_color):
        if self.check_btn.winfo_exists():
            self.check_btn.configure(bg=og_color)


    # method to check if the user input was correct or incorrect.
    def check(self):
        answer = self.meaning_entry.get()
        answer = answer.replace(" ", "")
        answer = answer.lower()
        meanings = self.meaning
        og_color = self.check_btn.cget("bg")
        
        # On correct answer
        meanings = [meaning.lower() for meaning in meanings]
        meanings = [meaning.replace(" ", "") for meaning in meanings]

        if answer in meanings:
            self.check_btn.config(bg = "green") # change button color to green to indicate correct answer to the user.
            self.test_frame.after(500, lambda: self.restore_button_color(og_color))
            
            self.meaning_entry.delete(0, tk.END)

            self.delete_entry()
            self.update_word_level(promote= True)
            if self.give_up_btn.winfo_ismapped():
                self.give_up_btn.grid_remove()
                self.meaning_label.grid_remove()
            
            word_exists = self.get_word()
            self.word_label.config(text= self.word)

            if word_exists == False:
                print("There are no words in the files")
                for widget in self.test_frame.winfo_children():
                    widget.destroy()
                tk.Label(self.test_frame, text= "All levels are empty. Please add words.", font= self.font,).grid(row= 2, column= 1, padx= 10, pady= 10)
                tk.Button(self.test_frame, text = "Back", font= self.font, width= 7,command= lambda: self.go_back(self.start_frame)).grid(row = 3, column=1,  padx= 10, pady= 10)
                self.test_frame.pack(fill= "both", expand=True)
                return

        # On incorrect answer
        else:
            #add the show feature for meaning
            self.check_btn.config(bg = "red") # change button color to red to indicate incorrect answer.
            self.test_frame.after(500, lambda: self.check_btn.configure(bg=og_color))
            self.meaning_entry.delete(0, tk.END)
            self.word_label.config(text= f"{self.word}")
            if not self.give_up_btn.winfo_ismapped():
                self.give_up_btn.grid()

            # Demote only if level > 1.
            if self.level > 1:
                self.delete_entry()
            self.update_word_level(promote= False)

    # Function to go back to the initial GUI
    def go_back(self, start_frame):
        self.test_frame.pack_forget()
        start_frame.pack(fill = "both", expand= True)
        del self

    def give_up(self):
        self.meaning_label.grid()
        self.meaning_label.config(text = ", ".join(self.meaning))

    # method to delete the word pair on correct or incorrect answer. Since .csv files cannot be edited in place in python,
    # we save the file to a dataframe, update the dataframe and then save it to a .csv file.
    def delete_entry(self):
        os.remove(f'Level_{self.level}.csv')
        self.df = self.df[self.df["word"] != self.word]
        self.df.to_csv(f'Level_{self.level}.csv', index=False)
    
    # method to promote or demote the word pair based on correct or incorrect answer by the user.
    def update_word_level(self, promote):
        if promote == True:
            # if level = 5, move word pair to archive
            if self.level == 5:
                added, unique_meaning = False, True
                with open(f"archive.csv", "r+", newline="", encoding="latin-1") as file:
                        reader = csv.reader(file, delimiter=",")
                        has_rows = any(reader)  # Check if there's at least one row
                        if has_rows:
                            for row in reader:
                                print(self.word), print(row)
                                if self.word == row[0]:
                                    added = True
                                    print("added")
                                    existing_meanings = set(row[1:])
                                    meaning_array_set = set(self.meaning)
                                    if not meaning_array_set.issubset(existing_meanings):
                                        self.meaning = existing_meanings.union(meaning_array_set) # using meaning_set converted to list as it removes the duplicates from the original.
                                    else:
                                        unique_meaning = False
                
                if added and unique_meaning:
                    file = f"archive.csv"
                    temp_file = f"archive.tmp"
                    with open(file, "r+", newline="", encoding="latin-1") as infile, \
                        open(temp_file, "a+", newline="", encoding="latin-1") as outfile:
                        
                            reader_2 = csv.reader(infile, delimiter=",")
                            writer = csv.writer(outfile, delimiter=",")
                            writer.writerows(row for row in reader_2 if row[0] != self.word)  # Fast filtering
                            writer.writerow([self.word] + list(self.meaning)) 
                    os.replace(temp_file, file)

                if added == False:
                    with open("archive.csv", "a+", newline= "") as archive:
                        writer = csv.writer(archive)
                        writer.writerow(self.pair)
                        archive.close()
            else:
                with open(f"Level_{self.level + 1}.csv", "a+", newline= "") as file:
                    writer = csv.writer(file)  
                    writer.writerow(self.pair)
                    file.close()
        else:
            # demote 
            if self.level > 1:
                with open(f"Level_{self.level - 1}.csv", "a+", newline= "") as file:
                    writer = csv.writer(file)
                    writer.writerow(self.pair)
                    file.close()

