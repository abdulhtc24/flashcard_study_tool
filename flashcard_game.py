import pandas as pd
from tkinter import *
import random
from tkinter import messagebox

# Load the Excel file
def load_flashcards(file_path):
    df = pd.read_excel(file_path)
    # Assuming columns A and B are the first two columns
    flashcards = df.iloc[:, :2].values.tolist()
    return flashcards

# Function to show the next flashcard
def show_next_flashcard():
    global flashcards, current_flashcard, correct_answers, total_questions, question_count
    if total_questions >= question_count:
        end_game()
        return
    for button in buttons:
        button.config(bg="SystemButtonFace", state=DISABLED)
    if flashcards:
        current_flashcard = random.choice(flashcards)
        flashcards.remove(current_flashcard)
        front_label.config(text=current_flashcard[0])
        back_label.config(text="")
        if is_multiple_choice:
            generate_multiple_choice()
    else:
        end_game()

# Function to show the answer
def show_answer():
    global current_flashcard
    if current_flashcard:
        back_label.config(text=current_flashcard[1])

# Function to generate multiple choice options
def generate_multiple_choice():
    global current_flashcard, flashcards
    choices = [current_flashcard[1]]
    while len(choices) < 4:
        choice = random.choice(flashcards)[1]
        if choice not in choices:
            choices.append(choice)
    random.shuffle(choices)
    for i, choice in enumerate(choices):
        buttons[i].config(text=f"{chr(65+i)}. {choice}", state=NORMAL)
        buttons[i].config(wraplength=500, anchor='w')

# Function to check the answer in multiple choice mode
def check_answer(choice):
    global current_flashcard, correct_answers, total_questions
    total_questions += 1
    correct_choice = current_flashcard[1]
    selected_choice = choice.split('. ')[1]
    if selected_choice == correct_choice:
        correct_answers += 1
        for button in buttons:
            if button.cget("text").endswith(correct_choice):
                button.config(bg="green")
            else:
                button.config(bg="red")
    else:
        for button in buttons:
            if button.cget("text").endswith(correct_choice):
                button.config(bg="green")
            elif button.cget("text").endswith(selected_choice):
                button.config(bg="red")
    root.after(1000, show_next_flashcard)

# Function to end the game
def end_game():
    global correct_answers, total_questions
    if is_multiple_choice:
        percentage_correct = (correct_answers / total_questions) * 100
        messagebox.showinfo("Game Over", f"You answered {percentage_correct:.2f}% correctly.")
    else:
        messagebox.showinfo("Game Over", "No more flashcards")
    root.destroy()

# Load flashcards
flashcards = load_flashcards('flashcards.xlsx')
current_flashcard = None

# Debug flag and question limit
debug_mode = False
question_count = 5 if debug_mode else len(flashcards)

is_multiple_choice = messagebox.askyesno("Game Mode", "Do you want to play the multiple-choice variant?")

# Initialize correct answer tracking
correct_answers = 0
total_questions = 0

# Setup the GUI
root = Tk()
root.title("Flashcard Game")

frame = Frame(root)
frame.pack(pady=20)

front_label = Label(frame, text="", font=("Helvetica", 18), wraplength=400)
front_label.pack(pady=20)

back_label = Label(frame, text="", font=("Helvetica", 18), wraplength=400)
back_label.pack(pady=20)

next_button = Button(frame, text="Next Flashcard", command=show_next_flashcard)
next_button.pack(pady=10)

show_button = Button(frame, text="Show Answer", command=show_answer)
show_button.pack(pady=10)

buttons_frame = Frame(root)
buttons_frame.pack(pady=20)

buttons = []
for i in range(4):
    button = Label(buttons_frame, text="", font=("Helvetica", 14), bg="SystemButtonFace", width=40, anchor='w', padx=10, pady=5, relief=RAISED)
    button.grid(row=i, column=0, pady=5)
    button.bind("<Button-1>", lambda event, i=i: check_answer(buttons[i].cget("text")))
    buttons.append(button)

# Start the game with the first flashcard
show_next_flashcard()

# Run the GUI loop
root.mainloop()
