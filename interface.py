import tkinter as tk
from tkinter import ttk
from Adder import Adder
from Tester import Tester

# Initial GUI
class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Ascend")
        root.geometry("700x400")

        large_font = ("Times", 25)

        self.start_frame = tk.Frame(root, bg="lightblue")
        tk.Label(self.start_frame, text="            Welcome to Word Ascend            ", font= large_font, bg="lightblue").grid(row= 0, columnspan= 3 , padx=10, pady=10)
        tk.Label(self.start_frame, text="To add a word to your vocabulary, press Add. \n Alternatively, press Test to test your knowledge.", font= large_font, bg="lightblue").grid(row= 1, columnspan= 3, rowspan=2, padx=10, pady=5)
        tk.Button(self.start_frame, text= "Add", font=large_font, width=7, command= lambda: self.show("Add")).grid(row= 4, column= 0, padx= 10, pady= 10)
        tk.Button(self.start_frame, text="Test", font= large_font, width=7, command= lambda: self.show("Test")).grid(row = 4, column= 1, padx=10, pady= 10)
        self.start_frame.pack(fill="both", expand=True)

    # method to handle  Add and Test buttonss
    def show(self, button):
        self.start_frame.pack_forget()

        if button == "Add":
            Adder(root= self.root, start_frame= self.start_frame)
        else:
            Tester(root= self.root, start_frame= self.start_frame)
            
    def run(self):
        self.root.mainloop()

gui = Interface(tk.Tk())
gui.run()


