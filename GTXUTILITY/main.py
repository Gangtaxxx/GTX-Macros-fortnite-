import customtkinter as ctk
import keyboard
import mouse
import json
import os
import threading
import time


# =========================
# THEME
# =========================

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")


BG = "#080808"
CARD = "#111111"
GREEN = "#00ff66"
GREEN_HOVER = "#00cc55"


# =========================
# CONFIG
# =========================

CONFIG_FILE = "config.json"


DEFAULT = {

    # Pickup
    "pickup_enabled": False,
    "pickup_key": "e",
    "pickup_delay": 20,


    # Pullout
    "pullout_enabled": False,
    "pullout_key": "f",


    # Sprint
    "sprint_enabled": False,
    "sprint_key": "shift",


    # Double
    "double_enabled": False,
    "double_trigger": "g",
    "double_edit": "r",
    "double_select": "t",


    # Crouch Spam
    "crouch_enabled": False,
    "crouch_trigger": "ctrl",
    "crouch_bind": "c",
    "crouch_delay": 50,


    # Drag Edit
    "drag_enabled": False,
    "drag_edit": "r",
    "drag_tile": "t"
}



def save(cfg):

    with open(CONFIG_FILE, "w") as f:

        json.dump(
            cfg,
            f,
            indent=4
        )



def load():

    if os.path.exists(CONFIG_FILE):

        with open(CONFIG_FILE, "r") as f:

            data = json.load(f)


        for key, value in DEFAULT.items():

            if key not in data:

                data[key] = value


        return data


    save(DEFAULT)

    return DEFAULT.copy()



config = load()



# =========================
# BOUTON CHOIX TOUCHE
# =========================


class KeyButton(ctk.CTkButton):


    def __init__(
        self,
        master,
        key_name,
        callback
    ):

        super().__init__(
            master,
            text=key_name.upper(),
            width=120,
            height=35,
            corner_radius=15,
            fg_color=GREEN,
            hover_color=GREEN_HOVER,
            text_color="black",
            command=self.listen
        )


        self.callback = callback



    def listen(self):

        self.configure(
            text="..."
        )


        def wait():


            key = keyboard.read_event().name


            self.callback(key)


            self.configure(
                text=key.upper()
            )



        threading.Thread(
            target=wait,
            daemon=True
        ).start()



# =========================
# APPLICATION
# =========================


app = ctk.CTk()

app.geometry(
    "600x750"
)

app.title(
    "GTX UTILITY"
)


app.configure(
    fg_color=BG
)



ctk.CTkLabel(
    app,
    text="GTX UTILITY",
    font=(
        "Segoe UI",
        32,
        "bold"
    ),
    text_color=GREEN
).pack(
    pady=20
)



# =========================
# MENU
# =========================


tab_menu = ctk.CTkFrame(
    app,
    fg_color=CARD,
    corner_radius=20
)

tab_menu.pack(
    fill="x",
    padx=20,
    pady=5
)



content = ctk.CTkFrame(
    app,
    fg_color=BG
)

content.pack(
    fill="both",
    expand=True
)



pages = {}



def show_page(name):

    for page in pages.values():

        page.pack_forget()


    pages[name].pack(
        fill="both",
        expand=True
    )



pickup_page = ctk.CTkFrame(
    content,
    fg_color=BG
)

pullout_page = ctk.CTkFrame(
    content,
    fg_color=BG
)

double_page = ctk.CTkFrame(
    content,
    fg_color=BG
)

crouch_page = ctk.CTkFrame(
    content,
    fg_color=BG
)

drag_page = ctk.CTkFrame(
    content,
    fg_color=BG
)



pages = {

    "Pickup": pickup_page,
    "Pullout": pullout_page,
    "Double": double_page,
    "Crouch Spam": crouch_page,
    "Drag Edit": drag_page

}



for name in pages:

    ctk.CTkButton(
        tab_menu,
        text=name,
        width=110,
        corner_radius=15,
        fg_color=GREEN,
        hover_color=GREEN_HOVER,
        text_color="black",
        command=lambda n=name: show_page(n)
    ).pack(
        side="left",
        padx=5,
        pady=5
    )



# =========================
# PICKUP PAGE
# =========================


ctk.CTkLabel(
    pickup_page,
    text="Pickup",
    font=(
        "Segoe UI",
        24,
        "bold"
    ),
    text_color=GREEN
).pack(
    pady=15
)



pickup_switch = ctk.CTkSwitch(
    pickup_page,
    text="Enable",
    progress_color=GREEN
)

pickup_switch.pack()



def pickup_key_changed(key):

    config["pickup_key"] = key
    save(config)



KeyButton(
    pickup_page,
    config["pickup_key"],
    pickup_key_changed
).pack(
    pady=10
)



pickup_slider = ctk.CTkSlider(
    pickup_page,
    from_=5,
    to=500,
    progress_color=GREEN,
    button_color=GREEN
)

pickup_slider.set(
    config["pickup_delay"]
)

pickup_slider.pack(
    fill="x",
    padx=40
)



pickup_label = ctk.CTkLabel(
    pickup_page,
    text=f"{config['pickup_delay']} ms"
)

pickup_label.pack()



def pickup_speed(value):

    value=int(value)

    config["pickup_delay"]=value

    pickup_label.configure(
        text=f"{value} ms"
    )

    save(config)



pickup_slider.configure(
    command=pickup_speed
)
# =========================
# PULLOUT + AUTO SPRINT
# =========================


ctk.CTkLabel(
    pullout_page,
    text="Pullout / Sprint",
    font=(
        "Segoe UI",
        24,
        "bold"
    ),
    text_color=GREEN
).pack(
    pady=15
)



# -------------------------
# ITEM PULLOUT
# -------------------------


ctk.CTkLabel(
    pullout_page,
    text="Item Pullout",
    font=(
        "Segoe UI",
        18,
        "bold"
    )
).pack()



pullout_switch = ctk.CTkSwitch(
    pullout_page,
    text="Enable",
    progress_color=GREEN
)

pullout_switch.pack(
    pady=5
)



def pullout_key_changed(key):

    config["pullout_key"] = key
    save(config)



KeyButton(
    pullout_page,
    config["pullout_key"],
    pullout_key_changed
).pack(
    pady=10
)



# -------------------------
# AUTO SPRINT
# -------------------------


ctk.CTkLabel(
    pullout_page,
    text="Auto Sprint",
    font=(
        "Segoe UI",
        18,
        "bold"
    )
).pack(
    pady=10
)



sprint_switch = ctk.CTkSwitch(
    pullout_page,
    text="Enable",
    progress_color=GREEN
)

sprint_switch.pack(
    pady=5
)



def sprint_key_changed(key):

    config["sprint_key"] = key
    save(config)



KeyButton(
    pullout_page,
    config["sprint_key"],
    sprint_key_changed
).pack(
    pady=10
)





# =========================
# DOUBLE
# =========================


ctk.CTkLabel(
    double_page,
    text="Double",
    font=(
        "Segoe UI",
        24,
        "bold"
    ),
    text_color=GREEN
).pack(
    pady=15
)



double_switch = ctk.CTkSwitch(
    double_page,
    text="Enable",
    progress_color=GREEN
)

double_switch.pack()



def double_trigger_changed(key):

    config["double_trigger"] = key
    save(config)



ctk.CTkLabel(
    double_page,
    text="Trigger"
).pack()



KeyButton(
    double_page,
    config["double_trigger"],
    double_trigger_changed
).pack(
    pady=5
)




def double_edit_changed(key):

    config["double_edit"] = key
    save(config)



ctk.CTkLabel(
    double_page,
    text="Edit Bind"
).pack()



KeyButton(
    double_page,
    config["double_edit"],
    double_edit_changed
).pack(
    pady=5
)




def double_select_changed(key):

    config["double_select"] = key
    save(config)



ctk.CTkLabel(
    double_page,
    text="Select Tile"
).pack()



KeyButton(
    double_page,
    config["double_select"],
    double_select_changed
).pack(
    pady=5
)
# =========================
# CROUCH SPAM
# =========================


ctk.CTkLabel(
    crouch_page,
    text="Crouch Spam",
    font=(
        "Segoe UI",
        24,
        "bold"
    ),
    text_color=GREEN
).pack(
    pady=15
)



crouch_switch = ctk.CTkSwitch(
    crouch_page,
    text="Enable",
    progress_color=GREEN
)

crouch_switch.pack(
    pady=5
)



def crouch_trigger_changed(key):

    config["crouch_trigger"] = key
    save(config)



ctk.CTkLabel(
    crouch_page,
    text="Activation Key"
).pack()



KeyButton(
    crouch_page,
    config["crouch_trigger"],
    crouch_trigger_changed
).pack(
    pady=10
)




def crouch_bind_changed(key):

    config["crouch_bind"] = key
    save(config)



ctk.CTkLabel(
    crouch_page,
    text="Crouch Bind"
).pack()



KeyButton(
    crouch_page,
    config["crouch_bind"],
    crouch_bind_changed
).pack(
    pady=10
)



crouch_slider = ctk.CTkSlider(
    crouch_page,
    from_=5,
    to=500,
    progress_color=GREEN,
    button_color=GREEN
)


crouch_slider.set(
    config["crouch_delay"]
)


crouch_slider.pack(
    fill="x",
    padx=40
)



crouch_label = ctk.CTkLabel(
    crouch_page,
    text=f"{config['crouch_delay']} ms"
)

crouch_label.pack(
    pady=5
)



def crouch_speed(value):

    value = int(value)

    config["crouch_delay"] = value

    crouch_label.configure(
        text=f"{value} ms"
    )

    save(config)



crouch_slider.configure(
    command=crouch_speed
)





# =========================
# DRAG EDIT
# =========================


ctk.CTkLabel(
    drag_page,
    text="Drag Edit",
    font=(
        "Segoe UI",
        24,
        "bold"
    ),
    text_color=GREEN
).pack(
    pady=15
)



drag_switch = ctk.CTkSwitch(
    drag_page,
    text="Enable",
    progress_color=GREEN
)

drag_switch.pack(
    pady=5
)




def drag_edit_changed(key):

    config["drag_edit"] = key
    save(config)



ctk.CTkLabel(
    drag_page,
    text="Edit Bind"
).pack()



KeyButton(
    drag_page,
    config["drag_edit"],
    drag_edit_changed
).pack(
    pady=10
)





def drag_tile_changed(key):

    config["drag_tile"] = key
    save(config)



ctk.CTkLabel(
    drag_page,
    text="Tile Bind"
).pack()



KeyButton(
    drag_page,
    config["drag_tile"],
    drag_tile_changed
).pack(
    pady=10
)
# =========================
# MACROS
# =========================


running = True



# -------------------------
# PICKUP SPAM
# -------------------------


def pickup_macro():

    while running:

        if pickup_switch.get():

            key = config["pickup_key"]


            if keyboard.is_pressed(key):

                keyboard.press_and_release(
                    key
                )


                time.sleep(
                    config["pickup_delay"] / 1000
                )


        time.sleep(0.01)





# -------------------------
# CROUCH SPAM
# -------------------------


def crouch_macro():

    while running:

        if crouch_switch.get():

            trigger = config["crouch_trigger"]


            if keyboard.is_pressed(trigger):

                keyboard.press_and_release(
                    config["crouch_bind"]
                )


                time.sleep(
                    config["crouch_delay"] / 1000
                )


        time.sleep(0.01)





# =========================
# MACROS
# =========================


running = True



# -------------------------
# PICKUP SPAM
# -------------------------

def pickup_macro():

    while running:

        if pickup_switch.get():

            key = config["pickup_key"]

            if keyboard.is_pressed(key):

                keyboard.press_and_release(key)

                time.sleep(
                    config["pickup_delay"] / 1000
                )


        time.sleep(0.01)





# -------------------------
# CROUCH SPAM
# -------------------------

def crouch_macro():

    while running:

        if crouch_switch.get():

            trigger = config["crouch_trigger"]

            if keyboard.is_pressed(trigger):

                keyboard.press_and_release(
                    config["crouch_bind"]
                )

                time.sleep(
                    config["crouch_delay"] / 1000
                )


        time.sleep(0.01)





# -------------------------
# DRAG EDIT
# -------------------------

def drag_edit_macro():

    edit_was_pressed = False
    select_is_down = False


    while running:


        if drag_switch.get():


            edit = config["drag_edit"]
            select = config["drag_tile"]


            edit_pressed = keyboard.is_pressed(edit)



            # EDIT DOWN

            if edit_pressed and not edit_was_pressed:


                # petite stabilisation pour Fortnite

                time.sleep(0.008)


                if not select_is_down:

                    keyboard.press(
                        select
                    )

                    select_is_down = True




            # EDIT UP

            elif not edit_pressed and edit_was_pressed:


                if select_is_down:


                    time.sleep(0.003)


                    keyboard.release(
                        select
                    )

                    select_is_down = False




            edit_was_pressed = edit_pressed




        else:


            if select_is_down:

                keyboard.release(
                    config["drag_tile"]
                )

                select_is_down = False


            edit_was_pressed = False




        time.sleep(0.001)





# -------------------------
# DOUBLE EDIT
# -------------------------

def double_macro():

    while running:

        if double_switch.get():

            trigger = config["double_trigger"]
            edit = config["double_edit"]
            select = config["double_select"]


            if keyboard.is_pressed(trigger):


                # PREMIER EDIT

                keyboard.press(edit)

                time.sleep(0.015)

                keyboard.release(edit)



                # PREMIER SELECT TILE

                keyboard.press(select)

                time.sleep(0.015)

                keyboard.release(select)



                # DELAI ENTRE LES DEUX EDITS

                time.sleep(0.020)



                # DEUXIEME EDIT

                keyboard.press(edit)

                time.sleep(0.015)

                keyboard.release(edit)



                # DEUXIEME SELECT TILE

                keyboard.press(select)

                time.sleep(0.015)

                keyboard.release(select)



                # RYTHME GLOBAL

                time.sleep(0.120)



            else:

                time.sleep(0.005)


        else:

            time.sleep(0.01)




# -------------------------
# SOURIS
# -------------------------

def mouse_action(event):

    if event.event_type == "up":


        if pullout_switch.get():

            keyboard.press_and_release(
                config["pullout_key"]
            )


        if sprint_switch.get():

            keyboard.press_and_release(
                config["sprint_key"]
            )





# -------------------------
# THREADS
# -------------------------

threading.Thread(
    target=pickup_macro,
    daemon=True
).start()



threading.Thread(
    target=crouch_macro,
    daemon=True
).start()



threading.Thread(
    target=drag_edit_macro,
    daemon=True
).start()



threading.Thread(
    target=double_macro,
    daemon=True
).start()



mouse.hook(
    mouse_action
)



# -------------------------
# DOUBLE
# -------------------------


def double_macro():

    while running:


        if double_switch.get():

            trigger = config["double_trigger"]


            if keyboard.is_pressed(trigger):


                keyboard.press_and_release(
                    config["double_edit"]
                )


                time.sleep(0.02)


                keyboard.press_and_release(
                    config["double_select"]
                )


                time.sleep(0.02)


        time.sleep(0.01)





# -------------------------
# SOURIS
# -------------------------


def mouse_action(event):

    if event.event_type == "up":


        if pullout_switch.get():

            keyboard.press_and_release(
                config["pullout_key"]
            )



        if sprint_switch.get():

            keyboard.press_and_release(
                config["sprint_key"]
            )





# =========================
# THREADS
# =========================


threading.Thread(
    target=pickup_macro,
    daemon=True
).start()



threading.Thread(
    target=crouch_macro,
    daemon=True
).start()



threading.Thread(
    target=drag_edit_macro,
    daemon=True
).start()



threading.Thread(
    target=double_macro,
    daemon=True
).start()



mouse.hook(
    mouse_action
)





# =========================
# SAUVEGARDE AUTO
# =========================


def update():


    config["pickup_enabled"] = bool(
        pickup_switch.get()
    )


    config["pullout_enabled"] = bool(
        pullout_switch.get()
    )


    config["sprint_enabled"] = bool(
        sprint_switch.get()
    )


    config["double_enabled"] = bool(
        double_switch.get()
    )


    config["crouch_enabled"] = bool(
        crouch_switch.get()
    )


    config["drag_enabled"] = bool(
        drag_switch.get()
    )



    save(config)



    app.after(
        200,
        update
    )





update()



show_page(
    "Pickup"
)



app.mainloop()