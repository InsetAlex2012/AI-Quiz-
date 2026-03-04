# https://github.com/TkinterEP/ttkthemes/tree/master/screenshots

import openai

from tkinter import *
from tkinter.ttk import *
from ttkthemes import ThemedTk

client = openai.OpenAI(api_key = "***ENTER YOUR API KEY HERE!***")

question_amount = 10

# =====================================================================

answer = None

score = 0

question_num = 0

def generate_question():
    global answer, question_num

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "Generate a simple yes/no question in English about technology, suitable for students, with a clear correct answer. Make the question unique every time and something that you would not accidentally say again, to make sure this doesn't happen, think of a difficult question. Not something like 'Do smartphones have touchscreens', or 'Are laptops considered computers?'. These are just examples. Also, make the questions difficult. Do not put a period on the end of the answer. Always keep the question under 40 characters long including spaces!!! Make sure this is ALWAYS under 40 characters!! This is the MOST important thing to do, NEVER FORGET to make it fit in 40 characters. ALWAYS AND ONLY return the format, nothing else, not even a 'Okay, heres the question': 'Question: <question> | Answer: <yes/no>' ."},
            {"role": "user", "content": "Generate a simple yes/no question."}
        ]
    )


    result = response.choices[0].message.content.strip()
    question_part, answer_part = result.split(" | ")
    question = question_part.replace("Question: ", "").strip()
    answer = answer_part.replace("Answer: ", "").strip().lower()
    print(question)
    print(answer)

    question_lbl.configure(text = question, background="light blue", font=("Rubik Mono One", 10))

    yes_button.configure(state = "enabled")
    no_button.configure(state = "enabled")

    question_num += 1


def check_answer(user_input):
    global score

    if user_input == answer:
        score += 1
        question_lbl.configure(text = "Correct!", background = "#00B824", font = ("Rubik Mono One", 25))
    else:
        question_lbl.configure(text = "Incorrect...", background = "#B30404", font = ("Rubik Mono One", 25))

    yes_button.configure(state = "disabled")
    no_button.configure(state = "disabled")


    if question_num < question_amount:
        root.after(3000, generate_question)
    else:
        root.after(3000, end)

def end():
    question_lbl.configure(text=f"Final Score: {score}/{question_amount}", background="light blue", font=("Rubik Mono One", 20))
    question_lbl.pack_forget()

    yes_button.pack_forget()
    no_button.pack_forget()

    question_answer_buttons_frame.pack_forget()


    question_lbl.pack(pady = 20)
    restart_button.pack()


def restart():
    global score, question_num

    score = 0
    question_num = 0

    restart_button.pack_forget()

    question_lbl.pack_forget()
    question_lbl.pack(pady = 20)

    question_answer_buttons_frame.pack(pady = 35)

    yes_button.pack(padx = 10, side = LEFT)
    no_button.pack(padx = 10, side = LEFT)

    generate_question()


# =====================================================================

root = ThemedTk(theme="breeze")

screen_width_middle = int(root.winfo_screenwidth() / 2 - 830 / 2)
screen_height_middle = int(root.winfo_screenheight() / 2 - 200 / 2)

root.geometry(f"830x200+{screen_width_middle}+{screen_height_middle}")
root.title("AI Quiz! - Python Project")
root.configure(themebg="breeze")
root.resizable(False, False)

# =====================================================================

question_lbl = Label(root, text = "", background="light blue", font=("Rubik Mono One", 10), justify="center")
question_lbl.pack(pady = 20)

# ---------------------------------------------------------------------

question_answer_buttons_frame = Frame(root)
question_answer_buttons_frame.pack(pady = 35)

answer_button_style = Style()
answer_button_style.configure("Answers.TButton", font = ("Rubik Mono One", 17))

# ---------------------------------------------------------------------

yes_button = Button(question_answer_buttons_frame, text = "Yes", style = "Answers.TButton", command = lambda: check_answer("yes"))
yes_button.pack(padx = 10, side = LEFT)

no_button = Button(question_answer_buttons_frame, text = "No", style = "Answers.TButton", command = lambda: check_answer("no"))
no_button.pack(padx = 10, side = LEFT)

restart_button = Button(root, text = "Restart!", style = "Answers.TButton", command = restart)



generate_question()



root.mainloop()