from customtkinter import *
from PIL import Image
from customtkinter import CTkImage
import webbrowser
import pyperclip
import json
from difflib import SequenceMatcher
from collections import Counter
import random
import sys
import os

class WysilfGUI():
    def clear_cards(self):
        for card in self.cards_list:
            card.destroy()
        self.cards_list.clear()

    def show_popup(self, messa):
        popup_message = CTkToplevel()
        popup_message.geometry("400x220")
        popup_message.title("Notice")
        popup_message.configure(fg_color="#18316b")

        popup_message.update_idletasks()
        x = (popup_message.winfo_screenwidth() // 2) - (400 // 2)
        y = (popup_message.winfo_screenheight() // 2) - (220 // 2)
        popup_message.geometry(f"+{x}+{y}")

        frame = CTkFrame(popup_message, corner_radius=20, fg_color="#143182")
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        label = CTkLabel(frame, text=f"{messa}", font=("Inter", 14, "bold"), text_color="#9fc7f7", wraplength=300, justify="center")
        label.pack(pady=(25, 15))

        button = CTkButton(frame, text="Got it!", font=("Inter", 14, "bold"), fg_color="#3b82f6",  hover_color="#60a5fa", text_color="white", corner_radius=12, command=popup_message.destroy)
        button.pack(pady=(0, 20))

        popup_message.transient(self.window)
        popup_message.lift()
    
    def helper(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        
        return os.path.join(os.path.abspath("."), relative_path)
    
    def load_up(self):
        self.clear_screen()

        bg_label = CTkLabel(self.window, image=self.bg_image, text="")
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        bg_label.lower()

        load_up_frame = CTkFrame(self.window, corner_radius=0, fg_color="#1e293b", width=500, height=500, border_width=12, border_color="#1F859C")
        load_up_frame.place(relx=0.5, rely=0.5, anchor="center")

        load_up_label = CTkLabel(load_up_frame, text="Welcome to Wysilf! - The Link Manager App", fg_color="#082e6b", text_color="#3b82f6", corner_radius=32, font=("Inter", 14, "bold"))
        load_up_label.place(relx=0.36, rely=0.06, anchor="center")

        login_btn = CTkButton(load_up_frame, text="Login - To Wysilf!", command=self.login_page, corner_radius=32, fg_color="#072A6C", hover_color="#083EA2", width=300, font=("Inter", 14))
        login_btn.place(relx=0.5, rely=0.68, anchor="center")

        signup_btn = CTkButton(load_up_frame, text="Sign Up - To Wysilf!", command=self.signup_page, corner_radius=32, fg_color="#072A6C", hover_color="#083EA2", width=300, font=("Inter", 14))
        signup_btn.place(relx=0.5, rely=0.6, anchor="center")
    
    def create_link_card(self, link, description, genre):
        card = CTkFrame(self.global_link_chat, fg_color="#1e293b", corner_radius=32)
        card.pack(fill="x", padx=10, pady=8)

        self.cards_list.append(card) 

        title = CTkLabel(card, text="Link Received", font=("Inter", 14, "bold"), text_color="#3b82f6")
        title.pack(anchor="w", padx=12, pady=(8, 2))

        link_label = CTkLabel(card, text=f"Link: {link} \nDescription: {description} / Genre: {genre}", wraplength=650, justify="left", text_color="white", cursor="hand2", font=("Inter", 14))
        link_label.pack(anchor="w", padx=12, pady=(0, 5))

        link_label.bind("<Button-1>", lambda e: self.tracker(genre) if webbrowser.open(link) else None)

        clear_btn = CTkButton(card, text="Clear", width=65, command=lambda: self.clear_spec_card(link))
        clear_btn.pack(side="right", padx=(0, 2))
        
        del_btn = CTkButton(card, text="Delete", width=65, command=lambda: self.del_link(link, card))
        del_btn.pack(side="right", padx=(0, 1))

        copy_btn = CTkButton(card, text="Copy", width=65, command=lambda: pyperclip.copy(link))
        copy_btn.pack(side="right")

        like_btn = CTkButton(card, image=self.img_photo, fg_color="transparent", bg_color="transparent", text="", width=35, command=lambda: self.tracker(genre))
        like_btn.pack(side="right", pady=(2, 0), padx=(0, 2))

        def on_enter(e): card.configure(fg_color="#2a3a55")
        def on_leave(e): card.configure(fg_color="#1e293b")

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
    
    def signup_page(self):
        self.clear_screen()

        bg_label = CTkLabel(self.window, image=self.bg_image, text="")
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        bg_label.lower()

        sign_up_frame = CTkFrame(self.window, corner_radius=0, fg_color="#1e293b", width=500, height=500, border_width=12, border_color="#1F859C")
        sign_up_frame.place(relx=0.5, rely=0.5, anchor="center")

        label_signup = CTkLabel(sign_up_frame, text="Please enter your new account details.", fg_color="#082e6b", text_color="#3b82f6", corner_radius=32, font=("Inter", 14, "bold"))
        label_signup.place(relx=0.19, rely=0.05)

        self.signup_entry_user = CTkEntry(sign_up_frame, placeholder_text="Insert username", width=300, font=("Inter", 14))
        self.signup_entry_user.place(relx=0.19, rely=0.44)

        self.signup_entry_pass = CTkEntry(sign_up_frame, placeholder_text="Insert password", width=300, font=("Inter", 14))
        self.signup_entry_pass.place(relx=0.19, rely=0.52)

        self.signup_entry_invite = CTkEntry(sign_up_frame, placeholder_text="Insert invite code", width=300, font=("Inter", 14))
        self.signup_entry_invite.place(relx=0.19, rely=0.6)

        submit_signup_btn = CTkButton(sign_up_frame, text="Submit.", command=self.starting_a_account, font=("Inter", 14, "bold"))
        submit_signup_btn.place(relx=0.20, rely=0.7)

        back_signup_btn = CTkButton(sign_up_frame, text="Back.", command=self.load_up, font=("Inter", 14, "bold"))
        back_signup_btn.place(relx=0.50, rely=0.7)

    def login_page(self):
        self.clear_screen()

        bg_label = CTkLabel(self.window, image=self.bg_image)
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        bg_label.lower()

        login_frame = CTkFrame(self.window, corner_radius=0, fg_color="#1e293b", width=500, height=500, border_width=12, border_color="#1F859C")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        label_login = CTkLabel(login_frame, text="Login to your account.", fg_color="#082e6b", text_color="#3b82f6", corner_radius=32, font=("Inter", 14, "bold"))
        label_login.place(relx=0.3, rely=0.05)

        self.login_entry_user  = CTkEntry(login_frame, placeholder_text="Insert username", width=300, font=("Inter", 14))
        self.login_entry_user.place(relx=0.19, rely=0.44)

        self.login_entry_pass = CTkEntry(login_frame, placeholder_text="Insert password", width=300, font=("Inter", 14))
        self.login_entry_pass.place(relx=0.19, rely=0.52)

        submit_login_btn = CTkButton(login_frame, text="Submit.", command=self.logging_in_to_a_account, font=("Inter", 14, "bold"))
        submit_login_btn.place(relx=0.20, rely=0.7)

        back_login_btn = CTkButton(login_frame, text="Back.", command=self.load_up, font=("Inter", 14, "bold"))
        back_login_btn.place(relx=0.50, rely=0.7)
    
    def main_page(self):
        self.clear_screen()

        bg_label = CTkLabel(self.window, image=self.bg_image)
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        bg_label.lower()
        
        self.global_link_chat = CTkScrollableFrame(self.window, width=750, height=550, corner_radius=0, fg_color="#0f172a", border_width=12, border_color="#1F859C")
        self.global_link_chat.place(relx=0.5, rely=0.4, anchor="center")

        self.frame_button_ctrl = CTkFrame(self.window, width=750, height=100,corner_radius=0, fg_color="#0f172a", border_width=12, border_color="#1F859C")
        self.frame_button_ctrl.place(relx=0.5, rely=0.9, anchor="center")
        
        rec_links_btn = CTkButton(self.frame_button_ctrl, text="Recommended Links.", command=self.rec_links, corner_radius=8, hover_color="#083EA2", fg_color="#072A6C", font=("Inter", 14, "bold"))
        rec_links_btn.place(relx=0.05, rely=0.5)

        add_link_btn = CTkButton(self.frame_button_ctrl, text="Add link.", command=self.add_link, corner_radius=8, hover_color="#083EA2", fg_color="#072A6C", font=("Inter", 14, "bold"))
        add_link_btn.place(relx=0.3, rely=0.5)

        taskbar_label = CTkLabel(self.frame_button_ctrl, text="Very Proffesional ToolBar", wraplength=300, justify="center", font=("Inter", 14, "bold"))
        taskbar_label.place(relx=0.35, rely=0.15)

        add_load_btn = CTkButton(self.frame_button_ctrl, text="Load Links.", command=self.load_saves, corner_radius=8, hover_color="#083EA2", fg_color="#072A6C", font=("Inter", 14, "bold"))
        add_load_btn.place(relx=0.5, rely=0.5)

        add_search_btn = CTkButton(self.frame_button_ctrl, text="Search Links.", command=self.search_link_popup, corner_radius=8, hover_color="#083EA2", fg_color="#072A6C", font=("Inter", 14, "bold"))
        add_search_btn.place(relx=0.7, rely=0.5)

class Savemachine():
    def save(self, link, description, genre):
        file_path = "saved_session.json"
        
        try:
            with open(file=file_path, mode="r") as file:
                cement = json.load(file)
        except:
            cement = {"accounts": self.accounts, "links": []}
        
        if "accounts" not in cement:
            cement["accounts"] = {}

        if "links" not in cement:
            cement["links"] = []

        if "recs_url" not in cement:
            cement["recs_url"] = []

        cement["links"].append({"link": link, "desc": description, "genre": genre})

        cement["accounts"] = self.accounts

        cement.setdefault("recs_url", []).append(genre)

        if len(cement["recs_url"]) >= 100:
            cement["recs_url"].clear()

        try:
            with open(file=file_path, mode="w") as file:
                json.dump(cement, file, indent=4)

        except:
            self.show_popup("ERROR TYPE 1: Save file not located")
            return

    def load_accounts(self):
        file_path = "saved_session.json"

        try:
            with open(file_path, "r") as file:
                valid = json.load(file)
                self.accounts = valid.get("accounts", {})

        except FileNotFoundError:
            self.accounts = {}

    def save_my_account(self, username, password):
        file_path = "saved_session.json"

        try:
            with open(file_path, "r") as file:
                valid = json.load(file)

        except FileNotFoundError:
            valid = {"accounts": {}, "links": []}

        self.accounts[username] = password
        valid["accounts"] = self.accounts    
        try:
            with open(file_path, "w") as file:
                json.dump(valid, file, indent=4)
        
        except FileNotFoundError:
            self.show_popup("ERROR TYPE 1: Save file not located")


    def load_saves(self):
        self.card_cleared.clear()
        file_path = "saved_session.json"
        try:
            with open(file_path, "r") as file:
                content = json.load(file)
                for item in content.get("links", []):
                    if item:
                        self.del_flag = False
                        self.create_link_card(item["link"], item["desc"], item["genre"])
                    
                    if not item:
                        self.show_popup("ERROR TYPE 1D: No links to load... Have you ever used the internet before?")
                
                self.accounts = content.get("accounts", {})

        except FileNotFoundError:
            self.show_popup("ERROR TYPE 1: Save file not located")

class WysilfWindow(WysilfGUI, Savemachine):
    def __init__(self):
        self.window = CTk()
        self.window.geometry("2000x1680")
        self.window.title("Wysilf - Verion 1.0")

        self.accounts = {}  
        self.cards_list = []
        self.tracker_list = []
        self.card_cleared = []
        
        img = Image.open(self.helper("thumbsup.jpg"))

        self.img_photo = CTkImage(light_image=img, dark_image=img, size=(35, 35))
        self.image_path = "bg.png"
        img = Image.open(self.helper("bg.png"))
        
        self.bg_image = CTkImage(light_image=img, dark_image=img, size=(2000,1680))

        set_appearance_mode("dark")

        self.tracker_list.append("Entertainment")
        self.load_accounts()
        self.load_up()   

    def clear_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def del_link(self, link, card):
        self.clear_cards()

        file_path = "saved_session.json"

        if card in self.cards_list:
            self.cards_list.remove(card)

        if link in self.tracker_list:
            self.tracker_list.remove(link)
        
        try:
            with open(file=file_path, mode="r") as file:
                pavement = json.load(file)

                for item in pavement.get("links", []):
                    if item["link"] == link:
                        pavement["links"] = [item for item in pavement["links"] if item["link"] != link]

        except:
            self.show_popup("ERROR TYPE 1: Issue deleting the link. Couldn't find save file")
            return
        
        try:
            with open(file=file_path, mode="w") as file:
                json.dump(pavement, file, indent=4)

        except:
            self.show_popup("ERROR TYPE 1: Save file not located")
            return
        
        self.load_saves()
    
    def clear_spec_card(self, link_spec):
        self.clear_cards()

        file_path = "saved_session.json"

        try:
            with open(file=file_path, mode="r") as file:
                pavement = json.load(file)

                for item in pavement.get("links", []):
                    link = item["link"]
                    desc = item["desc"]
                    genre = item["genre"]

                    if link != link_spec:
                        if link not in self.card_cleared:
                            self.create_link_card(link, desc, genre) 

                        else:
                            pass     
                    
                    else:
                        self.card_cleared.append(link)

        except:
            self.show_popup("ERROR TYPE 1: Issue deleting the link. Couldn't find save file")
            return
        

    def starting_a_account(self):
        username = self.signup_entry_user.get()
        password = self.signup_entry_pass.get()
        invite_code = self.signup_entry_invite.get()

        if not username or not password:
            self.show_popup("ERROR TYPE 3A:You must put in a user and a password!")
            return
        if username in self.accounts.keys():
            self.show_popup("ERROR TYPE 3B: Your username already exists!")
            return
        if len(password) < 8 or len(username) < 8:
            self.show_popup("ERROR TYPE 3C: Your password or username is too short")
            return
        if invite_code != "wysilf":
            self.show_popup("ERROR TYPE 3D: The invite code inputed is incorrect or wrong")
            return
        
        self.accounts[username] = password
        self.save_my_account(username, password)
        self.load_up()

        self.show_popup("Account successfully created!")

    def logging_in_to_a_account(self):
        self.load_accounts()

        username = self.login_entry_user.get()
        password = self.login_entry_pass.get()
        
        if username in self.accounts and self.accounts[username] == password:
            self.main_page()

        else:
            self.show_popup("ERROR TYPE 3E: Failed to login to the account!")
            return
    
    def search_link_popup(self):
        popup_message = CTkToplevel()
        popup_message.geometry("800x400")
        popup_message.title("Notice")
        popup_message.update()
        popup_message.resizable(False, False)

        label = CTkLabel(popup_message, text="Enter the link you wish to search!", wraplength=300, justify="center", font=("Inter", 14, "bold"))
        label.place(relx=0.5, rely=0.1, anchor="center")

        self.entry_searching_links = CTkEntry(popup_message, placeholder_text="Enter link.", width=300, font=("Inter", 14))
        self.entry_searching_links.place(relx=0.5, rely=0.3, anchor="center")
        
        self.combobox_genre_search = CTkComboBox(popup_message, values=["None", "Gaming", "Entertainment", "Creativity", "Art", "General", "Music"])
        self.combobox_genre_search.place(relx=0.5, rely=0.4, anchor="center")

        button = CTkButton(popup_message, text="Submit.", font=("Inter", 14, "bold"), fg_color="#6495e4",  hover_color="#3781dc", text_color="white", command=self.searching_links)
        button.place(relx=0.5, rely=0.6, anchor="center")

        popup_message.transient(self.window)
        popup_message.lift()
    
    chars = Counter([])
    def norm_link(self, link):
        if not link:
            self.show_popup("ERROR TYPE 2D: No link was given.")
            self.main_page()
            return None

        link = link.lower().strip()

        if link.startswith("https://www."):
            link = link[12:]

        elif link.startswith("http://www."):
            link = link[11:]

        elif link.startswith("https://"):
            link = link[8:]

        elif link.startswith("http://"):
            link = link[7:]

        return link
        
    def searching_links(self):
        links = []
        genre_specialized = self.combobox_genre_search.get()
        
        self.card_cleared.clear()

        file_path = "saved_session.json"
        try:
            with open(file=file_path, mode="r") as file:
                cement_links = json.load(file)
                try:
                    for item in cement_links["links"]:
                        links.append({"link": item["link"], "desc": item["desc"], "genre": item["genre"]})

                except:
                    self.show_popup("ERROR TYPE 1A: Failed to find read file")
                

        except FileNotFoundError:
            self.show_popup("ERROR TYPE 1: While searching for links we couldnt find your save file.")
            return

        link_search = self.entry_searching_links.get()

        if link_search:
           search = self.norm_link(self.entry_searching_links.get())

           over_score = 0
           over_link = None
           best_desc = None
           best_genre = None
        
        if not link_search:
            self.show_popup("ERROR TYPE UNKOWN: No search input given")
            return
        
        for item in links:
                score = SequenceMatcher(None, self.norm_link(item["link"]), search).ratio()

                if score > over_score:
                    over_score = score
                    over_link = item["link"]
                    best_desc = item["desc"]
                    best_genre = item["genre"]

        if over_score < 0.2:
                self.show_popup("No matching link found.")
                return

        if genre_specialized == "None" or genre_specialized == best_genre:
                self.clear_cards()
                self.create_link_card(over_link, best_desc, best_genre)

        else:
            self.show_popup("No links matched that genre.")
            
    def rec_links(self):
        self.clear_cards()
        self.card_cleared.clear()

        try:
            self.chars.update(self.tracker_list)
            char_mvp = self.chars.most_common(1)[0][0]

        except IndexError:
            self.show_popup("ERROR TYPE 4B: You must click at least one link so we can recommend more links!")
            return
        
        file_path = "saved_session.json"

        try:
            with open(file_path, "r") as file:
                content = json.load(file)

                self.clear_cards()

                duplicates_list = []
                for item in content.get("links", []):
                    ran_link_variety = random.randint(1, 3)
                    da_link = item.get("link")
                    da_desc = item.get("desc")
                    da_genre = item.get("genre")

                    recss = content.get("recs_url", [])

                    for ex_list in recss:
                        if len(recss) >= 50:
                            recss.clear()

                        else:
                            pass
                    
                    if da_genre == char_mvp:
                        if da_link not in duplicates_list:
                            duplicates_list.append(da_link)

                            self.chars.clear()
                            self.create_link_card(da_link, da_desc, da_genre)
                            
                    else:
                        pass
                    
                    if ran_link_variety == 1:
                        if da_link not in duplicates_list:
                            self.create_link_card(da_link, da_desc, da_genre)
                    
                    else:
                        pass
                    
                
        except FileNotFoundError:
            self.show_popup("ERROR TYPE 1: Save file not located.")

    def add_link(self):
        popup = CTkToplevel()
        popup.title("Add Link's - Wysilf")
        popup.geometry("800x400")
        popup.resizable(False, False)

        label_link = CTkLabel(popup, text="Enter link:", font=("Inter", 14, "bold"))
        label_link.pack(pady=10)

        entry_link = CTkEntry(popup, width=300, placeholder_text="Link", font=("Inter", 14))
        entry_link.pack(pady=5)

        entry_link_desc = CTkEntry(popup, width=300, placeholder_text="Description", font=("Inter", 14))
        entry_link_desc.pack(pady=5)

        combobox_genr1e = CTkComboBox(popup, values=["Gaming", "Entertainment", "Creativity", "Art", "General", "Music"])
        combobox_genr1e.pack(pady=5)

        def confirm():
            file_path = "saved_session.json"

            link = entry_link.get().strip()
            description = entry_link_desc.get().strip()
            genre = combobox_genr1e.get().strip()

            if link.startswith("https://") or link.startswith("www.") or link.startswith("http://"):
                try:
                    with open(file=file_path, mode="r") as file:
                        content = json.load(file)

                except FileNotFoundError:
                        content = {"links": []}

                if any(item["link"] == link for item in content.get("links", [])):
                    self.show_popup("ERROR TYPE 2A: Link already in service!")

                else:
                    self.save(link, description, genre)
                    self.create_link_card(link, description, genre)
                    popup.destroy()

            else:
                self.show_popup(f"ERROR TYPE 2B: The link: {link} Is improper")
                popup.destroy()

        def cancel():
            popup.destroy()
        
        confirm_btn = CTkButton(popup, text="Confirm", command=confirm, font=("Inter", 14, "bold"))
        confirm_btn.pack(pady=3)

        cancel_btn = CTkButton(popup, text="Cancel", command=cancel, font=("Inter", 14, "bold"))
        cancel_btn.pack(pady=3)

        popup.grab_set()
    
    def tracker(self, genre):
        self.tracker_list.append(genre)

        file_path = "saved_session.json"

        try:
            with open(file=file_path, mode="r") as file:
                cement = json.load(file)

        except:
            self.show_popup("ERROR TYPE 1: Save file not located")
            return
        
        cement.setdefault("recs_url", []).append(genre)
        
        with open(file_path, "w") as file:
            json.dump(cement, file, indent=4)

    def run_window(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = WysilfWindow()
    app.run_window()