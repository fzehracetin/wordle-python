import tkinter as tk
from tkinter import simpledialog
from turkishnlp import detector
from unicode_tr import unicode_tr
import sys

turkish_dict = detector.TurkishNLP()
turkish_dict.download()
turkish_dict.create_word_set()
def is_turkish(word):
    return turkish_dict.is_turkish(unicode_tr(word).lower())

class Gui():
    def __init__(self):
        self.colors = {
            "GREEN": "#6ca965",
            "YELLOW": "#c8b653",
            "LIGHT GRAY": "#eeeeee",
            "GRAY": "#787c7f",
            "BLACK": "#000000",
            "WHITE": "#ffffff",
        }
        self.letters = [
            ["E", "R", "T", "Y", "U", "I", "O", "P", "Ğ", "Ü"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Ş", "İ"],
            ["Z", "C", "V", "B", "N", "M", "Ö", "Ç"],
        ]

        self.keyboard_gui = { 
            "E": None, "R": None, "T": None, "Y": None, "U": None, "I": None, "O": None, "P": None, 
            "Ğ": None, "Ü": None,
            "A": None, "S": None, "D": None, "F": None, "G": None, "H": None, "J": None, "K": None, "L": None, 
            "Ş": None, "İ": None,
            "Z": None, "C": None, "V": None, "B": None, "N": None, "M": None, "Ö": None, "Ç": None, # Ö Ç
        }
        self.word_trials_gui = []
        self.trial_count = 0
        self.current_trial = ""
        self.current_trial_gui = []
        self.letters_tried = []
        self.notification_text = ""
        self.word = ""
             
        self.window = root  
        self.window.geometry("600x700")
        self.window.title("Wordle")
        self.window.bind('<KeyPress>', self.on_key_press)
        self.window.bind("<Return>", self.on_enter_pressed)
        self.window.bind("<BackSpace>", self.on_backspace_pressed)

        self.canvas = tk.Canvas(self.window, width=600, height=700, background="white")
        self.canvas.pack()

        self.draw_word_box(150, 50)
        self.draw_keyboard_box(40, 420)
        self.draw_notification_box(250, 640)
        self.get_user_input()

    def refresh_canvas(self):
        self.keyboard_gui = {
            "E": None, "R": None, "T": None, "Y": None, "U": None, "I": None, "O": None, "P": None,
            "Ğ": None, "Ü": None,
            "A": None, "S": None, "D": None, "F": None, "G": None, "H": None, "J": None, "K": None, "L": None, 
            "Ş": None, "İ": None,
            "Z": None, "C": None, "V": None, "B": None, "N": None, "M": None, "Ö": None, "Ç": None,
        }
        self.word_trials_gui = []
        self.trial_count = 0
        self.current_trial = ""
        self.current_trial_gui = []
        self.letters_tried = []
        self.notification_text = ""
        self.canvas.delete("all")
        self.draw_word_box(150, 50)
        self.draw_keyboard_box(40, 420)
        self.canvas.itemconfig(self.notification_text, text="")

    def on_key_press(self, event):
        letter = event.char
        if len(self.current_trial) < 5 and letter != " ":
            self.type_letter(unicode_tr(letter).upper())

    def on_backspace_pressed(self, event):
        # print("BACKSPACE")
        if len(self.current_trial) > 0:
            self.delete_letter()

    def on_enter_pressed(self, event):
        # print("ENTER")
        if len(self.current_trial) == 5 and is_turkish(self.current_trial):
            found = []
            for i in range(5):
                if self.current_trial[i] == self.word[i]:
                    self.fill_the_boxes(i, self.current_trial[i], "GREEN")
                    found.append(self.current_trial[i])
                elif self.current_trial[i] not in found and self.current_trial[i] in self.word:
                    self.fill_the_boxes(i, self.current_trial[i], "YELLOW")
                    found.append(self.current_trial[i])
                else:
                    self.fill_the_boxes(i, self.current_trial[i], "GRAY")
            if self.current_trial != self.word:
                self.current_trial = ""
                self.trial_count += 1
            else:
                self.canvas.itemconfig(self.notification_text, text="You won!")
                self.get_user_input()

            if self.trial_count == 6:
                self.canvas.itemconfig(self.notification_text, text="You lost! The word was " + self.word)
                self.get_user_input()

    def get_user_input(self):
        user_input = simpledialog.askstring("Input", "New word:")
        if len(user_input) == 5 and is_turkish(user_input):
            self.word = unicode_tr(user_input).upper()
            self.refresh_canvas()
        elif user_input.upper() == "EXIT":
            sys.exit()
        else:
            self.get_user_input()

    def retrieve_letter_box(self, index):
        # list of current trial gui elements
        current_trial_gui_list = self.word_trials_gui[self.trial_count]
        # get the letter box
        return current_trial_gui_list[index]

    def fill_the_boxes(self, index, letter, color):
        letter_box = self.retrieve_letter_box(index)
        self.canvas.itemconfig(letter_box, fill=self.colors[color])

        if letter not in self.letters_tried:
            key_box = self.keyboard_gui[letter]
            self.canvas.itemconfig(key_box, fill=self.colors[color])
            self.letters_tried.append(letter)

    def type_letter(self, letter):
        self.current_trial += letter
        letter_box = self.retrieve_letter_box(len(self.current_trial) - 1)
        rectangle_coords = self.canvas.coords(letter_box)

        letter_gui = self.canvas.create_text((rectangle_coords[0] + 25, rectangle_coords[1] + 25), 
                                        font=("Calibri bold", 18), 
                                        text=letter)
        self.current_trial_gui.append(letter_gui)

    def delete_letter(self):
        self.current_trial = self.current_trial[:-1]
        last_letter_gui = self.current_trial_gui[-1]
        self.current_trial_gui = self.current_trial_gui[:-1]
        self.canvas.delete(last_letter_gui)
        
    def draw_word_box(self, x, y):
        def draw_letter_square(x, y):
            return self.canvas.create_rectangle(x, y, x + 50, y + 50)

        def draw_rows_of_letters(x, y):
            letter_1 = draw_letter_square(x, y)
            letter_2 = draw_letter_square(x + 60, y)
            letter_3 = draw_letter_square(x + 120, y)
            letter_4 = draw_letter_square(x + 180, y)
            letter_5 = draw_letter_square(x + 240, y)
            return [letter_1, letter_2, letter_3, letter_4, letter_5]

        for i in range(6):
            self.word_trials_gui.append(draw_rows_of_letters(x, y))
            y += 60

    def draw_keyboard_box(self, start_x, start_y):
        def draw_keyboard_rectangle(x, y, letter, color):
            self.keyboard_gui[letter] = self.canvas.create_rectangle(x, y, x+40, y+60, 
                                                    fill=self.colors[color])
            ext = self.canvas.create_text((x + 20, y + 30), 
                                        font=("Calibri bold", 18), 
                                        text=letter) 
        def draw_row(letters, x, y):
            for letter in letters:
                color = "LIGHT GRAY"
                draw_keyboard_rectangle(x, y, letter, color)
                x += 45

        # draw the first row
        draw_row(self.letters[0], start_x + 35, start_y)
        # draw the second row
        draw_row(self.letters[1], start_x + 20, start_y + 65)
        # draw the third row
        draw_row(self.letters[2], start_x + 65, start_y + 130)

    def draw_notification_box(self, x, y):
        self.notification_text = self.canvas.create_text((x, y), 
                                        font=("Calibri bold", 15), 
                                        text="") 
        

if __name__ == "__main__":
    root = tk.Tk()
    gui = Gui()
    root.mainloop()