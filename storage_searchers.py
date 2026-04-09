import tkinter as tk
import random

inventory = {}
junk = ["vase","family scrapbook","old clothes","useless documents","sports equipment", "tools"]
filament = 100      #measured in grams
box_items_common = ["battery", "cables","power supply","speaker","circuit board",]
box_items_rare = [
    "graphics card", "ram", "processor", "hard drive", "monitor",
    "solid state drive", "motherboard", "mechanical keyboard"
    ]
valuables = {"vr headset":100,"vintage game console":100,"smart watch":250,"drone":350}
filament_cost = {"desktop computer":500,"bluetooth speaker":150,"bluetooth headphones":50,"laptop":350}
money = 1500
current_state = "main menu"
unit_prices = [150,300,500,600,800,1000]
unit_price_multiplier = [2,3,4]

def write(screen,text,newline=True,tag=None):
    screen.configure(state="normal")
    if newline:
        text += "\n"
    screen.insert(tk.END,text,tag)
    screen.configure(state="disabled")


def buy_unit(index,price,clicked_button):
    global money
    money -= price
    hud.config(text=f"${money}")
    clicked_button.config(state="disabled", text=f"Unit #{index+1}\nPURCHASED")


def play_game():
    background_screen.configure(state="normal")
    background_screen.configure(background="gray")
    background_screen.delete("1.0", tk.END)
    continue_button.place_forget()
    hud.place(rely=0.95,relx=0.5,anchor="center")

    # Create the invisible "cardboard box" to hold our buttons
    unit_frame = tk.Frame(root, bg="gray")

    # enumerate() gives us BOTH the position (index: 0, 1, 2...) AND the value (price: 150, 300...)
    for index, price in enumerate(unit_prices):
        # Check affordability: Set state to NORMAL if we have enough money, otherwise DISABLED
        btn_state = tk.NORMAL if money >= price else tk.DISABLED

        # Create the button inside unit_frame
        btn = tk.Button(unit_frame, text=f"Unit #{index + 1}\nPurchase for\n ${price}",
                        bg="white", fg="black", width=15, height=5, state=btn_state)

        # THE LAMBDA TRICK:
        # We take a "snapshot" of the current index (i=index), price (p=price), and button (b=btn).
        # We put them in an "envelope" (lambda) so buy_unit doesn't run until clicked.
        btn.configure(command=lambda i=index, p=price, b=btn: buy_unit(i, p, b))

        # THE GRID MATH:
        # Floor division (// 3) handles rows: keeps 3 items per row (0,0,0, 1,1,1)
        # Modulo (% 3) handles columns: cycles through 0, 1, 2 over and over
        btn.grid(row=index // 3, column=index % 3, padx=10, pady=10)

    unit_frame.place(relx=0.5, rely=0.5, anchor="center")
    write(background_screen, f"\n\n\nStorage Lot", True, "center")

def intro_screen():
    background_screen.configure(state="normal")
    background_screen.delete("1.0",tk.END)
    play_button.place_forget()
    quit_button.place_forget()
    settings_button.place_forget()
    continue_button.place(relx=0.5,rely=0.9,anchor="center",width=150,height=50)
    write(background_screen, f"\n\n\n\nWelcome to Storage Searchers, you've just lost \nyour job and taken everything out of your bank \naccount in order to fulfill a lifelong \ndream. Become rich. Buy a storage unit and pray \nto your god there's something valuable in it.", True, "center")

def quit_game():
    root.destroy()

def settings():
    background_screen.configure(state="normal")
    background_screen.delete("1.0",tk.END)
    play_button.place_forget()
    quit_button.place_forget()
    settings_button.place_forget()
    write(background_screen, "\nSettings", True, "center")


root =  tk.Tk()
root.title("Storage Searcher")
root.geometry("800x500")
root.configure(background="black")

background_screen = tk.Text(root, padx=5, pady=5, background="black", foreground="white", font=("Fixedsys", 18))
background_screen.pack(side="top", fill="x",expand=True)
write(background_screen, "\n\n\n\n Storage Searchers", True, "center")

hud = tk.Label(root,bg="gray",fg="white",text=f"${money}",font=("Fixedsys",16))

play_button = tk.Button(root, text="Play", command=intro_screen,background="white",foreground="black")
quit_button = tk.Button(root, text="Quit", command=quit_game,background="white",foreground="black")
settings_button = tk.Button(root, text="Settings", command=settings,background="white",foreground="black")
continue_button = tk.Button(root, text="Continue", command=play_game,background="white",foreground="black")


play_button.place(relx=0.5,rely=0.5,anchor="center", width=150,height=50)
quit_button.place(relx=0.5,rely=0.7,anchor="center",width=150,height=50)
settings_button.place(relx=0.5,rely=0.6,anchor="center",width=150,height=50)


background_screen.tag_configure("center", justify="center")

root.mainloop()