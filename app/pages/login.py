import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("truck", class_name="w-6 h-6 text-white"),
                    class_name="w-12 h-12 rounded-xl bg-blue-600 flex items-center justify-center shadow-inner",
                ),
                rx.el.h1(
                    "Trazo",
                    class_name="font-bold text-2xl tracking-tight italic text-slate-900 mt-4",
                ),
                class_name="flex flex-col items-center mb-8",
            ),
            rx.el.form(
                rx.el.h2(
                    "Iniciar Sesión",
                    class_name="text-xl font-bold text-center text-slate-900 mb-2",
                ),
                rx.el.p(
                    "Ingresa tus credenciales para acceder",
                    class_name="text-sm text-center text-slate-500 mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Usuario",
                        class_name="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2",
                    ),
                    rx.el.input(
                        placeholder="Ej: admin",
                        name="username",
                        class_name="w-full px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-100 outline-none transition-all text-slate-900 bg-white",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Contraseña",
                        class_name="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2",
                    ),
                    rx.el.input(
                        type="password",
                        placeholder="••••••••",
                        name="password",
                        class_name="w-full px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-100 outline-none transition-all text-slate-900 bg-white",
                    ),
                    class_name="mb-6",
                ),
                rx.cond(
                    AuthState.auth_error != "",
                    rx.el.p(
                        AuthState.auth_error,
                        class_name="text-red-500 text-sm mb-4 text-center",
                    ),
                ),
                rx.el.button(
                    "Ingresar",
                    type="submit",
                    class_name="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-xl shadow-lg active:scale-95 transition-all",
                ),
                on_submit=AuthState.login_submit,
                reset_on_submit=True,
            ),
            class_name="bg-white rounded-2xl border border-slate-200 shadow-sm p-8 w-full max-w-md animate-in fade-in zoom-in duration-500",
        ),
        class_name="min-h-screen flex items-center justify-center bg-slate-50 font-['Inter'] p-4",
    )