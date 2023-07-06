# ---------------------------- MODULS------------------------------- #
import random
from tkinter import *
import pandas

# ---------------------------- CONSTANTS ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"
FILE = "data/engsvk.csv"
UPDATED_FILE = "data/words_to_learn.csv"
ORIGINALLY_WORD = "English"
TRANSLATED_WORD = "Slovak"


# ---------------------------- FUNCTIONS ------------------------------- #


# Read csv file and insert into directory
def read_csv_into_directory():
    dictionary_pandas = []
    try:
        data = pandas.read_csv(UPDATED_FILE)
    except FileNotFoundError:
        data = pandas.read_csv(FILE)
    finally:
        dictionary_pandas = data.to_dict(orient="records")
    return dictionary_pandas


# Main Directory from csv file
word_directory = read_csv_into_directory()

# Current card
current_card = {}


# Generate new word for next card
def generate_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    # Choose random card from directory
    current_card = random.choice(word_directory)
    # Get english word from card
    eng_word = current_card[ORIGINALLY_WORD]
    # Set up canvas for current word
    canvas.itemconfig(card_word, text=eng_word, fill="black")
    canvas.itemconfig(card_title, text=ORIGINALLY_WORD, fill="black")
    canvas.itemconfig(card_image, image=card_front_image)
    # After 3s flip the card with translation
    flip_timer = window.after(3000, func=flip_card)


# Translate word
def flip_card():
    # change canvas
    canvas.itemconfig(card_image, image=card_back_image)
    canvas.itemconfig(card_word, text=current_card[TRANSLATED_WORD], fill="white")
    canvas.itemconfig(card_title, text=TRANSLATED_WORD, fill="white")


# Write to file unknown words
def write_to_file():
    word_directory.remove(current_card)
    df = pandas.DataFrame(word_directory)
    df.to_csv(UPDATED_FILE, index=False)



# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Flash card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(6000, func=flip_card)
# Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_image = PhotoImage(file="./images/card_front.png")
card_back_image = PhotoImage(file="./images/card_back.png")
card_image = canvas.create_image(400, 270, image=card_front_image)
card_title = canvas.create_text(400, 150, text="English", font=(FONT_NAME, 40, "italic"))
card_word = canvas.create_text(400, 253, text="word", font=(FONT_NAME, 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)
# RIGHT BUTTON
right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=lambda: [write_to_file(), generate_word()])
right_button.grid(row=1, column=1)
# WRONG BUTTON
wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=generate_word)
wrong_button.grid(row=1, column=0)

generate_word()

window.mainloop()
