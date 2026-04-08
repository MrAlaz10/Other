#imports tkinter, but lets us use just tk to refer to it
import tkinter as tk
import random


#in order to store memory, we need to use state management.
current_state = "main_menu"  #this variable creates a flag that keeps track of exactly what screen we are on
user_name = ""               #we need to be able to store the players name outside the function too
difficulty = {"easy" : 10,"medium" : 50,"hard" : 100}
difficulty_name = ""
difficulty_number = 0
current_answer = 0
current_score = 0
lives = 3
current_time = 0
time_limits = {"easy":10,"medium":15,"hard":20}
timer_job = 0

def process_command(event):
    global current_state,difficulty_number\
        ,difficulty,user_name, current_score,\
        current_answer,difficulty_name,\
        lives, timer_job,current_time                             #Tells the function to use the tracker variable from outside. Declare at the top of the function!
    user_input = entry_box.get().lower().strip(",./;'[]-= ")    #.get captures whatever string is sitting inside the entry widget .strip() removes whatever is passed as
    #deletes the text in the entry box                          # arguments, including spaces, so this removes these symbols and spaces from users input
    entry_box.delete(0, tk.END)
    if current_state == "main_menu":       #these 'states' act similar to while loops in tkinter
        if user_input == "play":
            terminal_screen.configure(state="normal")           #this unlocks the screen to allow text to be modified
            terminal_screen.delete("1.0", tk.END)        #clears the screen of the previous menu before redrawing new one
            terminal_screen.insert(tk.END, f"\n\n\n\nPlease enter your name:\n","center_text") #prints the user inputs
            terminal_screen.configure(state="disabled")         #relocks the screen
            current_state = "get_name"
        elif user_input == "leaderboards":
            terminal_screen.configure(state="normal")
            terminal_screen.delete("1.0", tk.END)
            terminal_screen.insert(tk.END,f"\n\n\n\nPlease type a difficulty or 'back' to go back:\n---Easy---\n---Medium---\n---Hard---\n---Back---\n","center_text")
            current_state = "get_leaderboards"
        elif user_input == "quit":
            root.quit()                                          #quit command!
        elif user_input == "tutorial":
            terminal_screen.configure(state="normal")
            terminal_screen.delete("1.0", tk.END)
            terminal_screen.insert(tk.END, f"""
            --- BINARY CHEAT SHEET ---

            VALUES:  128 | 64 | 32 | 16 | 8 | 4 | 2 | 1
            EXAMPLE:   0    1    0    0   1   0   0   1

            RULE: If it's a 1, add the value. If it's a
            0, ignore it.
            
            MATH: 64 + 8 + 1 = 73

            type 'back' to go back to main menu
            --------------------------
            """)
            terminal_screen.configure(state="disabled")
            current_state = "tutorial"
        else:
            error_message()
    elif current_state == "get_name":
        user_name = user_input                            #notice we can use the same entry_box.get().lower() by using the variable
        terminal_screen.configure(state="normal")
        terminal_screen.delete("1.0", tk.END)
        terminal_screen.insert(tk.END, f"\n\n\n\nPlease type a difficulty or 'back' to go back:\n---Easy---\n---Medium---\n---Hard---\n---Back---\n","center_text")
        terminal_screen.configure(state="disabled")
        current_state = "choose_difficulty"
    elif current_state == "choose_difficulty":
        if user_input in difficulty:
            difficulty_number = difficulty[user_input]
            difficulty_name = user_input
            current_time = time_limits[difficulty_name]
            current_score = 0
            lives = 3
            terminal_screen.pack_forget()
            hud.pack(side="top", pady=0, padx=5, fill="x")
            hud.config(text=f"Score: {current_score}    |    Lives: {lives}    |    Time: {current_time}")
            terminal_screen.pack(side="top", pady=0, padx=0, fill="both", expand=True)


            generate_next_question()          #dont be afraid to use functions
            start_timer()                     #start the timer!
            current_state = "play_game"       #always remember to change the state!
        elif user_input == "back":
            show_main_menu()
            current_state = "main_menu"  #always remember to change the state, even after a function!
        else:
            error_message()
    elif current_state == "play_game":
        try:
            user_input_int = int(user_input)
            if user_input_int == current_answer:
                current_score += 1
                terminal_screen.configure(state="normal")
                terminal_screen.insert(tk.END, f"\n\n\nCorrect!", "center_text")
                terminal_screen.configure(state="disabled")
                root.after(500,generate_next_question)    #root.after uses milliseconds to wait then executes the function in the second arg.
                current_time = time_limits[difficulty_name]
                # no () needed unless you need to pass in parameters
            else:
                lives -= 1
                if lives == 0:
                    game_over()
                else:
                    terminal_screen.configure(state="normal")
                    terminal_screen.delete("1.0", tk.END)
                    terminal_screen.insert(tk.END, f"\n\n\n\nSorry {user_name}, that's not correct!", "center_text")
                    terminal_screen.insert(tk.END,f"\n-1 life!", "center_text")
                    terminal_screen.configure(state="disabled")
                    root.after(1500,generate_next_question)
                    current_time = time_limits[difficulty_name]
        except ValueError:
            terminal_screen.configure(state="normal")
            terminal_screen.insert(tk.END, f"Integers only!\n")
            terminal_screen.configure(state="disabled")

    elif current_state == "get_leaderboards":
        leaderboards = []
        terminal_screen.configure(state="normal")
        terminal_screen.delete("1.0", tk.END)

        difficulty_name = user_input
        if user_input in difficulty:
            try:
                with open(f"leaderboards{difficulty_name}.txt", "r") as file:
                    for line in file:
                        line = line.strip()
                        line = line.split(",")
                        saved_name = line[0]
                        saved_score = int(line[1])
                        leaderboards.append([saved_name, saved_score])
            except FileNotFoundError:
                terminal_screen.configure(state="normal")
                terminal_screen.insert(tk.END, f"Error! You must play the game first to view leaderboard!\n")
                terminal_screen.configure(state="disabled")
                root.after(2000,show_main_menu)
                current_state = "main_menu"
                return        #we added a return here to go to main menu
            leaderboards.sort(key=lambda x: x[1], reverse=True)
            terminal_screen.insert(tk.END,f"----------------------LEADERBOARDS----------------------\n", "center_text")
            for record in leaderboards[:10]:   #we use list slicing to only display the top 10 results
                terminal_screen.insert(tk.END, f"Name: {record[0]}, Score: {record[1]}\n")
            terminal_screen.insert(tk.END,f"--------------------------------------------------------\n")
            terminal_screen.insert(tk.END, f"Type 'back' to go back to main menu.\n")
            terminal_screen.config(state="disabled")
        elif user_input == "back":
            show_main_menu()
            current_state = "main_menu"
        else:
            error_message()
    elif current_state == "tutorial":

        if user_input == "back":
                show_main_menu()
                current_state = "main_menu"
        else:
            error_message()

def game_over():
    global current_state,difficulty_name,user_name,current_score
    terminal_screen.configure(state="normal")
    terminal_screen.delete("1.0", tk.END)
    terminal_screen.insert(tk.END, f"\n\n\n\nGame Over! Score: {current_score}\n", "center_text")
    terminal_screen.configure(state="disabled")
    with open(f"leaderboards{difficulty_name}.txt", "a") as file:
            file.write(f"{user_name},{current_score}\n")



    root.after(3000,show_main_menu)
    current_state = "main_menu"

def error_message():
    terminal_screen.configure(state="normal")
    terminal_screen.insert(tk.END, f"Command not recognized\n")
    terminal_screen.configure(state="disabled")

def show_main_menu(): #clears the screen and shows the main menu
    hud.pack_forget()
    terminal_screen.configure(state="normal")
    terminal_screen.delete("1.0", tk.END)
    terminal_screen.insert(tk.END,
                           "\n\n\n\nWelcome to Binary Game 3: The TriSequel! \n\nPlease type to make a selection: \n\n--Play--\n--Tutorial--\n--Leaderboards--\n--Quit--\n\n",
                           "center_text")
    terminal_screen.configure(state="disabled")

def start_timer():
    global current_score,lives,timer_job, current_time
    hud.config(text=f"Score: {current_score}    |    Lives: {lives}    |    Time: {current_time}")

    if current_time > 0:
        current_time -= 1
        #loops the function until it reaches 0
        timer_job = root.after(1000, start_timer)
    else:
        lives -= 1
        if lives == 0:
            game_over()
        terminal_screen.configure(state="normal")
        terminal_screen.delete("1.0", tk.END)
        terminal_screen.insert(tk.END,f"\n\n\nTimes up!\n -1 life!\n", "center_text")
        terminal_screen.configure(state="disabled")
        #resets the clock for the next question
        current_time = time_limits[difficulty_name]
        root.after(1500,generate_next_question)
        #dont forget we have to restart timer too
        root.after(1500,start_timer)


def generate_next_question():
    global difficulty_number, current_answer, current_score
    current_answer = random.randint(1, difficulty_number)
    terminal_screen.configure(state="normal")
    terminal_screen.delete("1.0", tk.END)
    terminal_screen.pack_forget()
    hud.config(text=f"Score: {current_score}    |    Lives: {lives}    |    Time: {current_time}")
    terminal_screen.pack(side="top", pady=0, padx=0, fill="both", expand=True)
    terminal_screen.insert(tk.END, f"\n\n\n\n{bin(current_answer)}\n", "center_text")
    terminal_screen.configure(state="disabled")

#(Note: Functions triggered by Tkinter events automatically receive an event argument containing data about the key press or mouse click.
# Even if we don't use it, we have to put event in the parentheses, or Python will throw an error!)

#creates the main window ----- technically you can name it anything other than root, but its more traditional
root = tk.Tk()

#gives the window a title and starting size
root.title("Binary Game 3: The TriSequel")
root.geometry("800x500")
root.configure(bg="black")


#now to create an entry widget, tk.Entry, this lets the user type
#root tells what window its in, and the new argument at the end changes the colour of the blinking cursor to green
#We moved entry box above the terminal_screen so that it would draw it first, then the terminal_screen
entry_box = tk.Entry(root, bg="gray", fg="#00FF00", font=("Courier", 12), insertbackground="#00FF00")

hud = tk.Label(root,bg="black",fg="#00FF00",font=("Courier", 16))

#remember we don't want the entry box to be the whole screen, just stretch horizontally
#we need to tell tkinter to anchor the entry box to specific side of the screen, hence "bottom"
entry_box.pack(side="bottom",pady=0, padx=5, fill="x")

#hud.pack(side="top",pady=0, padx=5, fill="x")

#When we create a widget in tkinter, we always have to tell it two things: where it lives, and what it looks like.
#root tells what window the widget lives in, bg is the background color, fg is foreground color
terminal_screen = tk.Text(root, bg="black",fg="#00FF00", font=("Courier", 18))

#now you must "pack" the widget onto the screen, specify its location, "fill" allows the user to change the window size and the text keeps up
#you can use "both", "x", and "y" as arguments
#and we need to pack the screen to the top and let it expand to fill the remaining space
terminal_screen.pack(side="top",pady=0, padx=0, fill="both", expand=True)

#creating a tag to help with formatting
#"center_text" is just a name we came up with, it could be anything, justify="center" actually tells tkinter to align the text
terminal_screen.tag_configure("center_text",justify="center")
terminal_screen.tag_configure("right_align",justify="right")

#now that we created the tag, we can add it as a final argument in the .insert below

show_main_menu()
# .insert injects text into the widget, tk.END - This is the "index" (the location). It tells Tkinter, to add it to the end of what's already on the screen.
# terminal_screen.insert(tk.END, "\n\n\n\nWelcome to Binary Game 3: The TriSequel! \n\nPlease type to make a selection: \n\n--Play--\n--Leaderboards--\n--Quit--\n\n", "center_text")
#we need to stop the user from erasing the game!
#this will prevent code from writing to the text as well, so if we want to change it later, we need to re-enable 'state'
terminal_screen.config(state="disabled")


#GREAT QOL TIP ---- .focus() automatically places the blinking cursor in the box, without having to click
entry_box.focus()
#now we need to create a function that will be triggered by an action. see function above
#now that a function is created we need to bind a key to that function
# <Return> is the specific name for the enter key, process_command is the name of the function
root.bind("<Return>", process_command)

#start the event loop so the window stays open --- the window would close instantly otherwise
#---- MUST ALWAYS BE AT THE END OF GUI CODE
root.mainloop()
