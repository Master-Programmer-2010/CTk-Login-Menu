import os
from hashlib import sha256
from json import load, dump, JSONDecodeError
from re import search
from tkinter import filedialog
from uuid import uuid4

import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode("Dark")


class LoginMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.WIDTH = 500
        self.HEIGHT = 650
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.iconbitmap("Resources/window_icon.ico")
        self.resizable(False, False)
        self.attributes("-topmost", True)

        self.background_image = ctk.CTkImage(light_image=Image.open("Resources/background_image.png"),
                                             size=(1920, 1248))
        self.show_password_image = ctk.CTkImage(light_image=Image.open("Resources/show_password.png"), size=(25, 25))
        self.hide_password_image = ctk.CTkImage(light_image=Image.open("Resources/hide_password.png"), size=(25, 25))
        self.return_to_login_image = ctk.CTkImage(light_image=Image.open("Resources/return.png"), size=(20, 20))
        self.settings_image = ctk.CTkImage(light_image=Image.open("Resources/settings.png"), size=(20, 20))

        self.HOVER_BUTTON_FONT_STYLE = ctk.CTkFont(size=12, underline=False)

        self.underlined = False
        self.valid_username = False
        self.valid_password = False

        self.admin_username = "Admin"
        self.admin_password = "a44ca5d29f6dab4320ab986479fa985b2d584b11a7da934f7e80bb1449913a07"

        try:
            with open("Resources/database.json", "r") as file:
                data = load(file)
                if not data or not data.get("users"):
                    data = {"users": []}
        except (FileNotFoundError, JSONDecodeError):
            data = {"users": []}

        users = data.get("users", [])

        self.default_database_data = {
            "user_id": "71c50323-2963-4500-8807-832877200338",
            "username": self.admin_username,
            "password": self.admin_password,
            "deleted": False
        }

        if not users:
            try:
                with open("Resources/database.json", "r") as file:
                    data = load(file)
                    if not data or "users" not in data or not data["users"]:
                        data = {"users": [self.default_database_data]}
                    elif not any(user["username"] == "Admin" for user in data["users"]):
                        data["users"].append(self.default_database_data)
            except (FileNotFoundError, JSONDecodeError):
                data = {"users": [self.default_database_data]}

            with open("Resources/database.json", "w") as file:
                dump(data, file, indent=4)

        self.create_login_menu()

    def change_password_entry_visibility(self, reset=False, menu=None):
        if menu == 1:
            if reset or not self.show_password:
                self.password_change_state_button.configure(image=self.hide_password_image)
                self.password_entry.configure(show="\u2219")
            else:
                self.password_change_state_button.configure(image=self.show_password_image)
                self.password_entry.configure(show="")

        elif menu == 2:
            if reset or not self.show_password:
                self.password_change_state_button.configure(image=self.hide_password_image)
                self.password_entry.configure(show="\u2219")
                self.confirm_password_entry.configure(show="\u2219")
            else:
                self.password_change_state_button.configure(image=self.show_password_image)
                self.password_entry.configure(show="")
                self.confirm_password_entry.configure(show="")

        elif menu == 3:
            if reset or not self.show_password:
                self.password_change_state_button.configure(image=self.hide_password_image)
                self.reset_password_entry.configure(show="\u2219")
                self.confirm_reset_password_entry.configure(show="\u2219")
            else:
                self.password_change_state_button.configure(image=self.show_password_image)
                self.reset_password_entry.configure(show="")
                self.confirm_reset_password_entry.configure(show="")

        self.show_password = not self.show_password

    # login menu
    def create_login_menu(self):
        self.title("Login")
        self.bind("<Return>", lambda event: self.login_button_function())
        self.unbind("<Escape>")

        try:
            self.frame.destroy()
            self.background_image_label.destroy()
        except AttributeError:
            pass

        self.show_password = False

        self.background_image_label = ctk.CTkLabel(self, image=self.background_image, text="")
        self.background_image_label.place(x=-70, y=-20)

        self.frame = ctk.CTkFrame(self, width=350, height=410)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.menu_title = ctk.CTkLabel(self.frame, width=60, height=20, text="Log Into Your Account",
                                       font=ctk.CTkFont(family="Century Gothic", size=25, weight="bold"))
        self.menu_title.place(relx=0.5, y=45, anchor=ctk.CENTER)

        self.username_entry = ctk.CTkEntry(self.frame, width=240, placeholder_text="Username")
        self.username_entry.place(relx=0.5, y=125, anchor=ctk.CENTER)

        self.password_entry = ctk.CTkEntry(self.frame, width=240, placeholder_text="Password", show="\u2219")
        self.password_entry.place(relx=0.5, y=180, anchor=ctk.CENTER)

        self.entry_error = ctk.CTkLabel(self.frame, width=35, height=10, text="", justify=ctk.LEFT,
                                        font=ctk.CTkFont(size=12), text_color="#FF6347")
        self.entry_error.place(x=60, y=200)

        self.password_change_state_button = ctk.CTkButton(self.frame, width=32, height=32,
                                                          image=self.hide_password_image, fg_color="transparent",
                                                          hover=False, text="",
                                                          command=lambda: self.change_password_entry_visibility(menu=1))
        self.change_password_entry_visibility(reset=True, menu=1)
        self.password_change_state_button.place(x=294, y=164)

        self.login_button = ctk.CTkButton(self.frame, width=230, height=35, corner_radius=90, text="Login",
                                          command=self.login_button_function, font=ctk.CTkFont(size=14),
                                          fg_color="#1CA4B2", hover_color="#0E6E7C")
        self.login_button.place(relx=0.5, y=255, anchor=ctk.CENTER)

        self.line = ctk.CTkLabel(self.frame, width=250, height=5, text=f"{"\u2500" * 18} or {"\u2500" * 18}",
                                 font=ctk.CTkFont(family="Courier", size=12))
        self.line.place(relx=0.5, y=300, anchor=ctk.CENTER)

        self.sign_up_button = ctk.CTkButton(self.frame, width=230, height=35, corner_radius=90, text="Sign Up",
                                            command=self.create_sign_up_menu, font=ctk.CTkFont(size=14),
                                            fg_color="#B48A1E", hover_color="#8C6515")
        self.sign_up_button.place(relx=0.5, y=350, anchor=ctk.CENTER)

    def login_button_function(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = sha256(password.encode()).hexdigest()

        with open("Resources/database.json", "r") as file:
            data = load(file)
            users = data["users"]

        user = next((user for user in users if user["username"] == username), None)
        if user and user["password"] == hashed_password:
            if user["deleted"]:
                self.entry_error.configure(text="This Account Has Been Deleted!")
                with open("Resources/database.json", "r") as file:
                    data = load(file)
                    users = data["users"]

                index_to_remove = None
                for index, user in enumerate(users):
                    if user['username'] == username and user['password'] == hashed_password:
                        index_to_remove = index
                        break

                users.pop(index_to_remove)

                with open("Resources/database.json", "w") as file:
                    dump(data, file, indent=4)
            else:
                with open("Resources/database.json", "w") as file:
                    dump(data, file, indent=4)

                if username == self.admin_username and hashed_password == self.admin_password:
                    self.create_admin_menu()
                else:
                    self.destroy()
                    app = App(username, password)
                    app.mainloop()
        else:
            self.entry_error.configure(text="Password Or Username Incorrect.")

    # sign up menu
    def create_sign_up_menu(self):
        self.title("Sign Up")
        self.bind("<Return>", lambda event: self.sign_up_button_function())
        self.bind("<Escape>", lambda event: self.create_login_menu())

        self.HOVER_BUTTON_FONT_STYLE.configure(underline=False)

        try:
            self.frame.destroy()
            self.background_image_label.destroy()
        except AttributeError:
            pass

        self.show_password = False

        self.background_image_label = ctk.CTkLabel(self, image=self.background_image, text="")
        self.background_image_label.place(x=-70, y=-20)

        self.frame = ctk.CTkFrame(self, width=350, height=410)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.menu_title = ctk.CTkLabel(self.frame, width=60, height=20, text="Create Account",
                                       font=ctk.CTkFont(family="Century Gothic", size=25, weight="bold"))
        self.menu_title.place(relx=0.5, y=45, anchor=ctk.CENTER)

        self.username_entry = ctk.CTkEntry(self.frame, width=240, placeholder_text="Username")
        self.username_entry.place(relx=0.5, y=125, anchor=ctk.CENTER)

        self.password_entry = ctk.CTkEntry(self.frame, width=240, placeholder_text="Password", show="\u2219")
        self.password_entry.place(relx=0.5, y=180, anchor=ctk.CENTER)

        self.confirm_password_entry = ctk.CTkEntry(self.frame, width=240, placeholder_text="Confirm Password",
                                                   show="\u2219")
        self.confirm_password_entry.place(relx=0.5, y=235, anchor=ctk.CENTER)

        self.entry_error = ctk.CTkLabel(self.frame, width=35, height=10, text="", justify=ctk.LEFT,
                                        font=ctk.CTkFont(size=12), text_color="#FF6347")
        self.entry_error.place(x=60, y=257)

        self.password_change_state_button = ctk.CTkButton(self.frame, width=32, height=32,
                                                          image=self.hide_password_image, fg_color="transparent",
                                                          hover=False, text="",
                                                          command=lambda: self.change_password_entry_visibility(menu=2))
        self.change_password_entry_visibility(reset=True, menu=2)
        self.password_change_state_button.place(x=294, y=164)

        self.sign_up_button = ctk.CTkButton(self.frame, width=230, height=35, corner_radius=90, text="Sign Up",
                                            command=self.sign_up_button_function,
                                            font=ctk.CTkFont(size=14), fg_color="#B48A1E",
                                            hover_color="#8C6515")
        self.sign_up_button.place(relx=0.5, y=315, anchor=ctk.CENTER)

        self.return_to_login_menu_button = ctk.CTkButton(self.frame, width=50, height=10, text="Back to login?",
                                                         hover=False, fg_color="transparent",
                                                         command=self.create_login_menu,
                                                         font=self.HOVER_BUTTON_FONT_STYLE)
        self.return_to_login_menu_button.bind("<Enter>",
                                              lambda event: self.HOVER_BUTTON_FONT_STYLE.configure(underline=True))
        self.return_to_login_menu_button.bind("<Leave>",
                                              lambda event: self.HOVER_BUTTON_FONT_STYLE.configure(underline=False))
        self.return_to_login_menu_button.place(x=200, y=340)

    def sign_up_button_function(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        hashed_password = sha256(password.encode()).hexdigest()

        with open("Resources/database.json") as file:
            data = load(file)

        users = data["users"]
        for user in users:
            if user['username'] == username:
                self.entry_error.configure(text="This Username Is Taken.")
                self.valid_username = False
                return

        if username.isspace() or username == "":
            self.entry_error.configure(text="You Must Enter A Username.")
            self.valid_username = False
            return
        elif len(username) < 5:
            self.entry_error.configure(text="Username Must Be 5 Characters Or More.")
            self.valid_username = False
            return
        elif len(username) > 15:
            self.entry_error.configure(text="Username Must Under 15 Characters.")
            self.valid_username = False
            return
        elif " " in username:
            self.entry_error.configure(text="Username Must Not Contain Spaces.")
            self.valid_username = False
            return
        elif not search(r"[A-Z]", username):
            self.entry_error.configure(text="Username Must Contain At Least 1\nUpper Case Letter.")
            self.valid_username = False
            return
        elif not search(r"\d", username):
            self.entry_error.configure(text="Username Must Contain At Least 1 Digit.")
            self.valid_username = False
            return
        elif not search(r"[^\w\s]", username):
            self.entry_error.configure(text="Username Must Contain At Least 1 Symbol.")
            self.valid_username = False
            return
        else:
            self.entry_error.configure(text="")
            self.valid_username = True

        if password.isspace() or password == "":
            self.entry_error.configure(text="You Must Enter A Password.")
            self.valid_password = False
            return
        elif len(password) < 5:
            self.entry_error.configure(text="Password Must Be 5 Characters Or More.")
            self.valid_password = False
            return
        elif len(password) > 15:
            self.entry_error.configure(text="Password Must Under 15 Characters.")
            self.valid_password = False
            return
        elif " " in password:
            self.entry_error.configure(text="Password Must Not Contain Spaces.")
            self.valid_password = False
            return
        elif not search(r"[A-Z]", password):
            self.entry_error.configure(text="Password Must Contain At Least 1\nUpper Case Letter.")
            self.valid_password = False
            return
        elif not search(r"\d", password):
            self.entry_error.configure(text="Password Must Contain At Least 1 Digit.")
            self.valid_password = False
            return
        elif not search(r"[^\w\s]", password):
            self.entry_error.configure(text="Password Must Contain At Least 1 Symbol.")
            self.valid_password = False
            return
        elif password != confirm_password:
            self.entry_error.configure(text="Passwords Don't Match.")
            self.valid_password = False
            return
        else:
            self.entry_error.configure(text="")
            self.valid_password = True

        if username == password:
            self.valid_username, self.valid_password = False, False
            self.entry_error.configure(text="Password Can't Be Same As Username.")
            self.valid_username = False

        if self.valid_username and self.valid_password:
            user_id = str(uuid4())
            while any(user["user_id"] == user_id for user in users):
                user_id = str(uuid4())

            new_user = {
                "user_id": user_id,
                "username": username,
                "password": hashed_password,
                "deleted": False
            }
            users.append(new_user)
            data["users"] = users

            with open("Resources/database.json", "w") as file:
                dump(data, file, indent=4)

            self.create_login_menu()

    # admin menu
    def create_admin_menu(self, user_num_reset=True):
        self.title("Admin Menu")
        self.unbind("<Return>")
        self.unbind("<Escape>")

        try:
            self.frame.destroy()
            self.background_image_label.destroy()
        except AttributeError:
            pass

        with open("Resources/database.json", "r") as file:
            data = load(file)

        usernames = [user["username"] for user in data["users"] if
                     user["username"] != "Admin" and not user["deleted"] is True]
        usernames_count = len(usernames)

        self.frame = ctk.CTkFrame(self, corner_radius=0)
        self.frame.pack(fill="both", expand=True)

        self.main_frame = ctk.CTkFrame(self.frame, width=472, height=300)
        self.main_frame.place(relx=0.5, y=376, anchor=ctk.S)

        self.scroll_frame = ctk.CTkScrollableFrame(self.frame, width=450, height=200)
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        self.scroll_frame.grid_columnconfigure(1, weight=1)
        self.scroll_frame.place(relx=0.5, y=620, anchor=ctk.S)

        self.return_button = ctk.CTkButton(self.frame, width=35, height=35, text="",
                                           fg_color="#696969", hover_color="#505050",
                                           command=self.create_login_menu,
                                           image=self.return_to_login_image)
        self.return_button.place(x=15, y=20)

        self.settings_button = ctk.CTkButton(self.frame, width=35, height=35, text="",
                                             fg_color="#696969", hover_color="#505050",
                                             command=self.create_settings_menu,
                                             image=self.settings_image)
        self.settings_button.place(x=450, y=20)

        self.menu_title = ctk.CTkLabel(self.frame, width=60, height=20, text="Admin",
                                       font=ctk.CTkFont(family="Century Gothic", size=25, weight="bold"))
        self.menu_title.place(relx=0.5, y=35, anchor=ctk.CENTER)

        for i in range(usernames_count):
            select_username_label = ctk.CTkLabel(master=self.scroll_frame, text=f"{usernames[i]}", justify=ctk.LEFT,
                                                 font=ctk.CTkFont(size=18, weight="bold"))
            select_username_label.grid(row=i, column=0, padx=20, pady=10, sticky=ctk.W)
            username_select_button = ctk.CTkButton(master=self.scroll_frame, width=90, height=20, text="Select",
                                                   font=ctk.CTkFont(size=18, weight="bold"),
                                                   fg_color="#008B8B", hover_color="#006666",
                                                   command=lambda num=i: self.select_username(num))
            username_select_button.grid(row=i, column=1, padx=20, pady=10, sticky=ctk.S)

        self.username_label = ctk.CTkLabel(self.main_frame, text=f"Username:",
                                           font=ctk.CTkFont(size=18, weight="bold"), justify=ctk.LEFT)
        self.username_label.place(x=15, y=20)

        self.json_textbox = ctk.CTkTextbox(self.main_frame, width=400, height=170, state=ctk.DISABLED,
                                           font=ctk.CTkFont(size=13), cursor="arrow")
        self.json_textbox.place(relx=0.5, y=150, anchor=ctk.CENTER)

        self.reset_password_button = ctk.CTkButton(self.main_frame, text="Reset Password", fg_color="#008B8B",
                                                   hover_color="#006666", font=ctk.CTkFont(size=15, weight="bold"),
                                                   command=self.reset_password_button_function)
        self.reset_password_button.place(relx=0.3, y=270, anchor=ctk.CENTER)

        self.remove_account_button = ctk.CTkButton(self.main_frame, text="Remove User", fg_color="#008B8B",
                                                   hover_color="#006666", font=ctk.CTkFont(size=15, weight="bold"),
                                                   command=self.remove_account_button_function)
        self.remove_account_button.place(relx=0.7, y=270, anchor=ctk.CENTER)

        if user_num_reset:
            self.user_index = None
        else:
            self.select_username(user_num=self.user_index)

    def select_username(self, user_num):
        with open("Resources/database.json", "r") as file:
            data = load(file)
            usernames = [user["username"] for user in data["users"] if
                         user["username"] != "Admin" and not user["deleted"] is True]

            username = usernames[user_num]
            for user in data["users"]:
                if user["username"] == username:
                    json_user_data = "\n".join(f"{key}: {value}" for key, value in user.items())

        self.username_label.configure(text=f"Username: {username}")
        self.json_textbox.configure(state=ctk.NORMAL)
        self.json_textbox.delete("0.0", "end")
        self.json_textbox.insert("0.0", json_user_data)
        self.json_textbox.configure(state=ctk.DISABLED)

        self.user_index = user_num

        try:
            self.select_user_warning_label.destroy()
        except AttributeError:
            pass

    def reset_password_button_function(self):
        if self.user_index is not None:
            self.json_textbox.destroy()
            self.reset_password_button.destroy()
            self.remove_account_button.destroy()

            self.reset_password_entry = ctk.CTkEntry(self.main_frame, width=350, placeholder_text="New Password")
            self.reset_password_entry.place(relx=0.5, y=100, anchor=ctk.CENTER)

            self.confirm_reset_password_entry = ctk.CTkEntry(self.main_frame, width=350,
                                                             placeholder_text="Confirm Password")
            self.confirm_reset_password_entry.place(relx=0.5, y=150, anchor=ctk.CENTER)

            self.confirm_password_reset_button = ctk.CTkButton(self.main_frame, width=160, text="Confirm Reset",
                                                               fg_color="#008B8B", hover_color="#006666",
                                                               font=ctk.CTkFont(size=15, weight="bold"),
                                                               command=self.reset_password)
            self.confirm_password_reset_button.place(relx=0.3, y=215, anchor=ctk.CENTER)

            self.cancel_password_reset_button = ctk.CTkButton(self.main_frame, width=160, text="Cancel Reset",
                                                              fg_color="#008B8B", hover_color="#006666",
                                                              font=ctk.CTkFont(size=15, weight="bold"),
                                                              command=lambda: self.create_admin_menu(
                                                                  user_num_reset=False))
            self.cancel_password_reset_button.place(relx=0.7, y=215, anchor=ctk.CENTER)

            self.entry_error = ctk.CTkLabel(self.main_frame, width=35, height=10, text="", justify=ctk.LEFT,
                                            font=ctk.CTkFont(size=12), text_color="#FF6347")
            self.entry_error.place(x=65, y=170)

            self.password_change_state_button = ctk.CTkButton(self.main_frame, width=32, height=32,
                                                              fg_color="transparent", image=self.hide_password_image,
                                                              hover=False, text="",
                                                              command=lambda: self.change_password_entry_visibility(
                                                                  menu=3))
            self.show_password = False
            self.change_password_entry_visibility(reset=True, menu=3)
            self.password_change_state_button.place(x=412, y=84)
        else:
            self.select_user_warning()

    def remove_account_button_function(self, yes_button_clicked=False):
        if yes_button_clicked:
            with open("Resources/database.json", "r") as file:
                data = load(file)
                data["users"][self.user_index + 1]["deleted"] = True

            with open("Resources/database.json", "w") as file:
                dump(data, file, indent=4)

            try:
                self.are_you_sure_label.destroy()
                self.yes_button.destroy()
                self.no_button.destroy()
            except AttributeError:
                pass

            self.are_you_sure_label = ctk.CTkLabel(self.main_frame, text="Account Deleted",
                                                   font=ctk.CTkFont(size=22, weight="bold"))
            self.are_you_sure_label.place(relx=0.5, y=160, anchor=ctk.CENTER)

            self.user_index = None

            self.after(1500, self.create_admin_menu)
        elif self.user_index is not None:
            self.json_textbox.destroy()
            self.reset_password_button.destroy()
            self.remove_account_button.destroy()

            self.are_you_sure_label = ctk.CTkLabel(self.main_frame, text="Are You Sure?",
                                                   font=ctk.CTkFont(size=18, weight="bold"))
            self.are_you_sure_label.place(relx=0.5, y=120, anchor=ctk.CENTER)

            self.yes_button = ctk.CTkButton(self.main_frame, width=160, text="Yes", fg_color="#008B8B",
                                            hover_color="#006666", font=ctk.CTkFont(size=15, weight="bold"),
                                            command=lambda: self.remove_account_button_function(
                                                yes_button_clicked=True))
            self.yes_button.place(relx=0.3, y=215, anchor=ctk.CENTER)

            self.no_button = ctk.CTkButton(self.main_frame, width=160, text="No", fg_color="#008B8B",
                                           hover_color="#006666", font=ctk.CTkFont(size=15, weight="bold"),
                                           command=lambda: self.create_admin_menu(user_num_reset=False))
            self.no_button.place(relx=0.7, y=215, anchor=ctk.CENTER)
        else:
            self.select_user_warning()

    def reset_password(self):
        reset_password = self.reset_password_entry.get()
        confirm_reset_password = self.confirm_reset_password_entry.get()
        hashed_reset_password = sha256(reset_password.encode()).hexdigest()
        with open("Resources/database.json", "r") as file:
            data = load(file)
            usernames = [user["username"] for user in data["users"] if
                         user["username"] != "Admin" and not user["deleted"] is True]
            username = usernames[self.user_index]

        if reset_password.isspace() or reset_password == "":
            self.entry_error.configure(text="You Must Enter A Password.")
            self.valid_password = False
            return
        elif len(reset_password) < 5:
            self.entry_error.configure(text="Password Must Be 5 Characters Or More.")
            self.valid_password = False
            return
        elif len(reset_password) > 15:
            self.entry_error.configure(text="Password Must Under 15 Characters.")
            self.valid_password = False
            return
        elif " " in reset_password:
            self.entry_error.configure(text="Password Must Not Contain Spaces.")
            self.valid_password = False
            return
        elif not search(r"[A-Z]", reset_password):
            self.entry_error.configure(text="Password Must Contain At Least 1\nUpper Case Letter.")
            self.valid_password = False
            return
        elif not search(r"\d", reset_password):
            self.entry_error.configure(text="Password Must Contain At Least 1 Digit.")
            self.valid_password = False
            return
        elif not search(r"[^\w\s]", reset_password):
            self.entry_error.configure(text="Password Must Contain At Least 1 Symbol.")
            self.valid_password = False
            return
        elif username == reset_password:
            self.valid_username, self.valid_password = False, False
            self.entry_error.configure(text="Password Can't Be Same As Username.")
            self.valid_username = False
        elif reset_password != confirm_reset_password:
            self.entry_error.configure(text="Passwords Don't Match.")
            self.valid_password = False
            return
        else:
            self.entry_error.configure(text="")
            self.valid_password = True

        if self.valid_password:
            data["users"][self.user_index + 1]["password"] = hashed_reset_password

            with open("Resources/database.json", "w") as file:
                dump(data, file, indent=4)

            self.create_admin_menu(user_num_reset=False)

    def select_user_warning(self):
        self.select_user_warning_label = ctk.CTkLabel(self.main_frame, text="Select User First", justify=ctk.LEFT,
                                                      font=ctk.CTkFont(size=18, weight="bold"), text_color="#FF6347")
        self.select_user_warning_label.place(x=117, y=20)

    # admin settings menu
    def create_settings_menu(self):
        self.title("Admin Menu")
        self.unbind("<Return>")
        self.unbind("<Escape>")

        try:
            self.frame.destroy()
            self.background_image_label.destroy()
        except AttributeError:
            pass

        self.frame = ctk.CTkFrame(self, corner_radius=0)
        self.frame.pack(fill="both", expand=True)

        self.main_frame = ctk.CTkFrame(self.frame, width=472, height=544)
        self.main_frame.place(relx=0.5, y=76, anchor=ctk.N)

        self.return_button = ctk.CTkButton(self.frame, width=35, height=35, text="",
                                           fg_color="#696969", hover_color="#505050",
                                           command=self.create_admin_menu,
                                           image=self.return_to_login_image)
        self.return_button.place(x=15, y=20)

        self.menu_title = ctk.CTkLabel(self.frame, width=60, height=20, text="Settings",
                                       font=ctk.CTkFont(family="Century Gothic", size=25, weight="bold"))
        self.menu_title.place(relx=0.5, y=35, anchor=ctk.CENTER)

        self.json_textbox = ctk.CTkTextbox(self.main_frame, width=400, height=400, font=ctk.CTkFont(size=13),
                                           cursor="arrow")
        with open("Resources/database.json", "r") as file:
            data = load(file)

            formatted_data = ""
            for item in data["users"]:
                for key, value in item.items():
                    formatted_data += f"{key}: {value}\n"
                formatted_data += "\n" * 2

        self.json_textbox.insert("0.0", formatted_data)
        self.json_textbox.configure(state=ctk.DISABLED)
        self.json_textbox.place(relx=0.5, y=40, anchor=ctk.N)

        self.export_database_button = ctk.CTkButton(self.main_frame, width=170, text="Export Database",
                                                    fg_color="#008B8B", hover_color="#006666",
                                                    font=ctk.CTkFont(size=15, weight="bold"),
                                                    command=self.export_database)
        self.export_database_button.place(relx=0.255, y=485, anchor=ctk.CENTER)

        self.reset_database_button = ctk.CTkButton(self.main_frame, width=170, text="Reset Database",
                                                   fg_color="#008B8B", hover_color="#006666",
                                                   font=ctk.CTkFont(size=15, weight="bold"),
                                                   command=self.reset_database)
        self.reset_database_button.place(relx=0.745, y=485, anchor=ctk.CENTER)

    @staticmethod
    def export_database():
        with open("Resources/database.json", "r") as file:
            data = load(file)

        export_to = filedialog.asksaveasfilename(initialfile="database.json", title="Export Location",
                                                 filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        if export_to:
            export_dir = os.path.dirname(export_to)
            if export_dir:
                os.makedirs(export_dir, exist_ok=True)

            with open(export_to, 'w') as json_file:
                dump(data, json_file, indent=4)

    def reset_database(self, confirm=False):
        if confirm:
            with open("Resources/database.json", 'w') as file:
                dump({"users": [self.default_database_data]}, file, indent=4)

            self.are_you_sure_label.configure(text="Database Reset")
            try:
                self.return_button.destroy()
                self.confirm_button.destroy()
            except AttributeError:
                pass
            self.after(1500, self.create_admin_menu)
        else:
            try:
                self.json_textbox.destroy()
                self.export_database_button.destroy()
                self.reset_database_button.destroy()
            except AttributeError:
                pass

            self.are_you_sure_label = ctk.CTkLabel(self.main_frame, text="Are You Sure?",
                                                   font=ctk.CTkFont(size=22, weight="bold"))
            self.are_you_sure_label.place(relx=0.5, y=210, anchor=ctk.CENTER)

            self.return_button = ctk.CTkButton(self.main_frame, width=170, text="Return",
                                               fg_color="#008B8B", hover_color="#006666",
                                               font=ctk.CTkFont(size=15, weight="bold"),
                                               command=self.create_settings_menu)
            self.return_button.place(relx=0.745, y=335, anchor=ctk.CENTER)

            self.confirm_button = ctk.CTkButton(self.main_frame, width=170, text="Confirm",
                                                fg_color="#008B8B", hover_color="#006666",
                                                font=ctk.CTkFont(size=15, weight="bold"),
                                                command=lambda: self.reset_database(confirm=True))
            self.confirm_button.place(relx=0.255, y=335, anchor=ctk.CENTER)


class App(ctk.CTk):
    def __init__(self, username, password):
        super().__init__()
        self.geometry("500x500")

        label = ctk.CTkLabel(self, text=f"username: {username}\npassword: {password}")
        label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)


if __name__ == "__main__":
    try:
        login_menu = LoginMenu()
        login_menu.mainloop()
    except KeyboardInterrupt:
        pass
