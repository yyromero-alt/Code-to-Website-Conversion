import reflex as rx
import bcrypt
from datetime import datetime
from typing import TypedDict
from app.shared_store import SharedStore


class UserData(TypedDict):
    username: str
    password_hash: str
    role: str
    created_at: str


class AuthState(rx.State):
    username: str = ""
    password: str = ""
    confirm_password: str = ""
    is_authenticated: bool = False
    current_user: str = ""
    current_role: str = ""
    auth_error: str = ""
    is_loading: bool = False
    users_list: list[dict[str, str]] = []
    new_user_username: str = ""
    new_user_password: str = ""
    new_user_role: str = "viewer"
    show_create_user_form: bool = False

    @rx.var
    def is_admin(self) -> bool:
        return self.current_role == "admin"

    @rx.event
    def set_new_user_username(self, value: str):
        self.new_user_username = value

    @rx.event
    def set_new_user_password(self, value: str):
        self.new_user_password = value

    @rx.event
    def set_new_user_role(self, value: str):
        self.new_user_role = value

    @rx.event
    def toggle_create_user_form(self):
        self.show_create_user_form = not self.show_create_user_form

    @rx.event
    def check_auth_status(self):
        if not self.is_authenticated or self.current_user == "":
            return rx.redirect("/login")

    @rx.event
    def check_login_page(self):
        if self.is_authenticated and self.current_user != "":
            return rx.redirect("/")

    @rx.event
    def login_submit(self, form_data: dict):
        self.auth_error = ""
        username = form_data.get("username", "").strip()
        password = form_data.get("password", "").strip()
        if not username or not password:
            self.auth_error = "Por favor, ingresa usuario y contraseña"
            return
        user = SharedStore.find_user(username)
        if user:
            if bcrypt.checkpw(
                password.encode("utf-8"), user["password_hash"].encode("utf-8")
            ):
                self.is_authenticated = True
                self.current_user = user["username"]
                self.current_role = user["role"]
                self.username = ""
                self.password = ""
                return rx.redirect("/")
            else:
                self.auth_error = "Usuario o contraseña incorrectos"
        else:
            self.auth_error = "Usuario o contraseña incorrectos"

    @rx.event
    def login(self):
        self.auth_error = ""
        if not self.username or not self.password:
            self.auth_error = "Por favor, ingresa usuario y contraseña"
            return
        user = SharedStore.find_user(self.username)
        if user:
            if bcrypt.checkpw(
                self.password.encode("utf-8"),
                user["password_hash"].encode("utf-8"),
            ):
                self.is_authenticated = True
                self.current_user = user["username"]
                self.current_role = user["role"]
                self.username = ""
                self.password = ""
                return rx.redirect("/")
            else:
                self.auth_error = "Usuario o contraseña incorrectos"
        else:
            self.auth_error = "Usuario o contraseña incorrectos"

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.current_user = ""
        self.current_role = ""
        self.username = ""
        self.password = ""
        return rx.redirect("/login")

    @rx.event
    def load_users(self):
        self.users_list = [
            {
                "username": u["username"],
                "role": u["role"],
                "created_at": u.get("created_at", ""),
            }
            for u in SharedStore.get_users()
        ]

    @rx.event
    def create_user(self):
        if self.current_role != "admin":
            return rx.toast("No tienes permisos para crear usuarios.")
        if not self.new_user_username or not self.new_user_password:
            return rx.toast("El usuario y la contraseña son obligatorios.")
        if SharedStore.find_user(self.new_user_username) is not None:
            return rx.toast("El usuario ya existe.")
        hashed = bcrypt.hashpw(
            self.new_user_password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        new_user: UserData = {
            "username": self.new_user_username,
            "password_hash": hashed,
            "role": self.new_user_role,
            "created_at": datetime.now().isoformat(),
        }
        SharedStore.add_user(new_user)
        self.new_user_username = ""
        self.new_user_password = ""
        self.new_user_role = "viewer"
        self.show_create_user_form = False
        self.load_users()
        return rx.toast("Usuario creado con éxito.")

    @rx.event
    def delete_user(self, username: str):
        if self.current_role != "admin":
            return rx.toast("No tienes permisos para eliminar usuarios.")
        if username == self.current_user:
            return rx.toast("No puedes eliminarte a ti mismo.")
        SharedStore.remove_user(username)
        self.load_users()
        return rx.toast("Usuario eliminado con éxito.")