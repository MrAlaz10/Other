import tkinter as tk
import random

#------SAVED DATA-------
inventory = {}
filament = 100      #measured in grams
money = 100
items_crafted = 0
items_sold = 0
storage_units_opened = 0
boxes_opened = 0
old_3d_printer = False
tutorial_completed = True
current_state = ""
purchased_units = []
#---------LOOT--------------
junk = ["broken vase","family scrapbook","old clothes","useless documents"," damaged sports equipment", "rusty tools"]
box_items_common = [
    "small battery", "cables","power supply","small speaker",
    "circuit board", "large speaker", "medium battery", "computer fan"]
box_items_rare = [
    "graphics card", "ram", "processor", "hard drive", "monitor",
    "solid state drive", "motherboard", "mechanical keyboard"
    ]
box_items_legendary = [
    "vr headset",
    "vintage game console",
    "smart watch",
    "drone"
]
valuables_price = {
    # --- Common Items ---
    "cables": 2,
    "small battery": 3,
    "circuit board": 4,
    "small speaker": 5,
    "computer fan": 6,
    "medium battery": 8,
    "power supply": 12,
    "large speaker": 15,

    # --- Rare Items ---
    "mechanical keyboard": 25,
    "ram": 30,
    "hard drive": 35,
    "solid state drive": 45,
    "motherboard": 50,
    "monitor": 60,
    "processor": 75,
    "graphics card": 90,

    # --- Crafted / High-End Valuables ---
    "bluetooth headphones": 50,
    "vr headset": 100,
    "vintage game console": 100,
    "bluetooth speaker": 100,
    "important documents": 200,
    "smart watch": 250,
    "drone": 350,
    "desktop computer": 1000,
    "laptop": 1200
}
filament_cost = {"desktop computer":500,"bluetooth speaker":150,"bluetooth headphones":50,"laptop":350}
#--------------OTHER-----------------
active_boxes = {}
unit_prices = [150,300,500,600,800,1000]
unit_price_multiplier = [2.0,2.50,3]
box_colors = {1 : "burlywood", 2 : "peru", 3 : "tan", 4 : "saddlebrown"}


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
    global current_state
    current_state = "main lot"
    background_screen.configure(state="normal")
    background_screen.configure(background="gray")
    background_screen.delete("1.0", tk.END)
    continue_button.place_forget()
    inventory_button.place(relx=0.7,rely=0.9,width=150,height=50)

    #hud.place(rely=0.95,relx=0.5,anchor="center")

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

def tutorial_unit():
    global boxes_opened, current_state
    current_state = "tutorial"
    background_screen.config(state="normal")
    background_screen.delete("1.0", tk.END)
    background_screen.config(bg="dimgray")
    hud.place(rely=0.95, relx=0.5, anchor="center")
    continue_button.place_forget()
    inventory_button.place(relx=0.7,rely=0.9,width=150,height=50)
    write(background_screen, "\nGrandpa's Storage", True, "center")
    spawn_boxes(6)

def generate_loot(amount_to_roll):
    rolled_items = []
    for index in range(amount_to_roll):
        percentage = random.uniform(0.0,1.0)
        if percentage < 0.6:
            rolled_items.append(random.choice(junk))
        elif percentage < 0.9:
            rolled_items.append(random.choice(box_items_common))
        elif percentage < 0.98:
            rolled_items.append(random.choice(box_items_rare))
        else:
            rolled_items.append(random.choice(box_items_legendary))
    return rolled_items

def open_box(button):
    global boxes_opened, filament, old_3d_printer, active_boxes
    boxes_opened += 1
    button.place_forget()
    del active_boxes[button]
    items_amount = random.randint(3, 5)
    if boxes_opened == 10:
        loot = ["old 3D printer", "used filament spool"]
        filament += 100
        old_3d_printer = True
    else:
        loot = generate_loot(items_amount)
        for item in loot:
            if item in inventory:
                inventory[item] += 1
            elif item in junk:
                pass
            else:
                inventory[item] = 1
    for item in loot:
        write(background_screen, f"\n{item}", True, "center")
    if boxes_opened == 6:
        continue_button.config(command=play_game)
        continue_button.place(relx=0.3,rely=0.9,anchor="center",width=150,height=50)

def show_inventory():
    global boxes_opened, active_boxes
    if current_state != "main lot":
        for box in active_boxes:
            box.place_forget()
    elif current_state == "main lot":
        unit_frame.place_forget()
    background_screen.config(state="normal")
    background_screen.delete("1.0", tk.END)
    background_screen.config(bg="black")
    inventory_back_button.place(relx=0.7,rely=0.9,width=150,height=50)
    write(background_screen, f"\n\n{inventory}\n\n\n{boxes_opened}", True, "center")

def return_from_inventory():
    global active_boxes, current_state
    if current_state == "tutorial":
        background_screen.config(state="normal")
        background_screen.delete("1.0", tk.END)
        background_screen.config(bg="dimgray")
        hud.place(rely=0.95, relx=0.5, anchor="center")
        inventory_back_button.place_forget()
        inventory_button.place(relx=0.7,rely=0.9,width=150,height=50)
        write(background_screen, "\nGrandpa's Storage", True, "center")
    elif current_state == "main lot":
        background_screen.configure(state="normal")
        background_screen.configure(background="gray")
        background_screen.delete("1.0", tk.END)
        continue_button.place_forget()
        unit_frame.place(relx=0.5, rely=0.5, anchor="center")
        inventory_button.place(relx=0.7, rely=0.9, width=150, height=50)
        write(background_screen, f"\n\n\nStorage Lot", True, "center")
    for box in active_boxes:
        box.place(relx=active_boxes[box][0], rely=active_boxes[box][1])


def spawn_boxes(max_amount):
    global box_colors, active_boxes
    safe_zones = [(0.2, 0.2), (0.5, 0.3), (0.8, 0.2), (0.2,0.6),(0.5, 0.8),(0.8, 0.5),(0.4,0.5),(0.8,0.8)]
    for index in range(max_amount):
        base_x = safe_zones[index][0]
        base_y = safe_zones[index][1]
        random_location_x = base_x + random.uniform(-0.06, 0.05)
        random_location_y = base_y + random.uniform(-0.06, 0.05)
        random_height = random.randint(4, 5)
        random_width = random.randint(4, 8)
        box_color_picker = random.randint(1, 4)
        box_button = tk.Button(root, text="Open", bg=box_colors[box_color_picker], fg="white", font=("Fixedsys", 14),
                               width=random_width, height=random_height)
        box_button.config(command= lambda b=box_button: open_box(b))
        box_button.place(relx=random_location_x, rely=random_location_y)
        active_boxes[box_button] = (random_location_x, random_location_y)
    hud.lift()

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
root.geometry("800x700")
root.configure(background="black")

background_screen = tk.Text(root, padx=5, pady=5, background="black", foreground="white", font=("Fixedsys", 18))
background_screen.pack(side="top", fill="x",expand=True)
write(background_screen, "\n\n\n\n Storage Searchers", True, "center")

hud = tk.Label(root,bg="gray",fg="white",text=f"${money}",font=("Fixedsys",16))

inventory_label = tk.Label(root,bg="black",fg="white",font=("Fixedsys",16))

play_button = tk.Button(root, text="Play", command=intro_screen,background="white",foreground="black")
quit_button = tk.Button(root, text="Quit", command=quit_game,background="white",foreground="black")
settings_button = tk.Button(root, text="Settings", command=settings,background="white",foreground="black")
continue_button = tk.Button(root, text="Continue", command=tutorial_unit,background="white",foreground="black")
inventory_button = tk.Button(root, text="Inventory", command=show_inventory,background="white",foreground="black")
inventory_back_button = tk.Button(root, text="Back", command=return_from_inventory,background="white",foreground="black")

# Create the invisible "cardboard box" to hold our buttons for main lot
unit_frame = tk.Frame(root, bg="gray")

play_button.place(relx=0.5,rely=0.5,anchor="center", width=150,height=50)
quit_button.place(relx=0.5,rely=0.7,anchor="center",width=150,height=50)
settings_button.place(relx=0.5,rely=0.6,anchor="center",width=150,height=50)


background_screen.tag_configure("center", justify="center")

root.mainloop()
