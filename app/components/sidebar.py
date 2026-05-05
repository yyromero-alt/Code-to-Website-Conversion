import reflex as rx
from app.states.docu_state import DocuState
from app.states.auth_state import AuthState


def nav_item(
    label: str, icon_name: str, tab_id: str, badge: str = ""
) -> rx.Component:
    is_active = DocuState.active_tab == tab_id
    events = [DocuState.set_tab(tab_id)]
    if tab_id == "admin":
        events.append(AuthState.load_users)
    return rx.el.button(
        rx.el.div(
            rx.icon(
                icon_name,
                class_name=rx.cond(
                    is_active, "w-5 h-5", "w-5 h-5 text-slate-400"
                ),
            ),
            rx.el.span(label),
            class_name="flex items-center gap-3",
        ),
        rx.cond(
            badge != "",
            rx.el.span(
                badge,
                class_name=rx.cond(
                    is_active,
                    "text-[10px] px-1.5 py-0.5 rounded bg-blue-400 text-white",
                    "text-[10px] px-1.5 py-0.5 rounded bg-slate-200 text-slate-500",
                ),
            ),
        ),
        on_click=events,
        class_name=rx.cond(
            is_active,
            "w-full flex items-center justify-between px-4 py-3 rounded-xl transition-all duration-200 text-sm font-medium bg-blue-600 text-white shadow-lg",
            "w-full flex items-center justify-between px-4 py-3 rounded-xl transition-all duration-200 text-sm font-medium text-slate-500 hover:bg-slate-100",
        ),
    )


def sidebar_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("truck", class_name="w-6 h-6 text-white"),
                class_name="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center shadow-inner",
            ),
            rx.el.h1(
                "Trazo",
                class_name="font-bold text-xl tracking-tight italic text-slate-900",
            ),
            class_name="p-8 border-b border-slate-100 flex items-center gap-3",
        ),
        rx.el.nav(
            rx.el.p(
                "General",
                class_name="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-4 mb-2",
            ),
            nav_item("Documentos", "file-text", "documentos"),
            nav_item("Paquetería", "package", "envios"),
            rx.el.p(
                "Módulos",
                class_name="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-4 mt-6 mb-2",
            ),
            nav_item(
                "Seguimiento Lista",
                "layout-list",
                "seguimiento_v1",
                badge="Original",
            ),
            nav_item(
                "Seguimiento Detalle", "truck", "seguimiento_v2", badge="Nuevo"
            ),
            nav_item("Inventarios", "boxes", "inventarios"),
            rx.cond(
                AuthState.is_admin,
                rx.fragment(
                    rx.el.p(
                        "Sistema",
                        class_name="text-[10px] font-bold text-slate-400 uppercase tracking-widest px-4 mt-6 mb-2",
                    ),
                    nav_item("Administración", "settings", "admin"),
                ),
            ),
            class_name="flex-1 p-6 space-y-2 overflow-y-auto",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("user", class_name="w-5 h-5 text-slate-600"),
                    class_name="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center flex-shrink-0",
                ),
                rx.el.div(
                    rx.el.p(
                        AuthState.current_user,
                        class_name="text-sm font-bold text-slate-900 truncate",
                    ),
                    rx.el.span(
                        AuthState.current_role,
                        class_name=rx.cond(
                            AuthState.is_admin,
                            "bg-blue-50 text-blue-600 px-2 py-0.5 rounded text-[10px] font-bold uppercase",
                            "bg-slate-100 text-slate-500 px-2 py-0.5 rounded text-[10px] font-bold uppercase",
                        ),
                    ),
                    class_name="flex-1 min-w-0",
                ),
                class_name="flex items-center gap-3 mb-4",
            ),
            rx.el.button(
                rx.icon("log-out", class_name="w-4 h-4"),
                rx.el.span("Cerrar Sesión"),
                on_click=AuthState.logout,
                class_name="w-full flex items-center justify-center gap-2 py-2 text-sm font-bold text-slate-500 hover:bg-slate-100 hover:text-slate-900 rounded-xl transition-colors",
            ),
            class_name="p-4 border-t border-slate-100",
        ),
        class_name="flex flex-col h-full bg-white",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        sidebar_content(),
        class_name="hidden lg:flex w-72 border-r border-slate-200 flex-col h-screen sticky top-0",
    )


def mobile_sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            on_click=DocuState.toggle_sidebar,
            class_name=rx.cond(
                DocuState.is_sidebar_open,
                "fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 transition-opacity",
                "hidden",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    rx.icon("x", class_name="w-6 h-6"),
                    on_click=DocuState.toggle_sidebar,
                    class_name="absolute top-4 right-4 p-2 text-slate-400 hover:text-slate-600",
                ),
                sidebar_content(),
                class_name="h-full relative",
            ),
            class_name=rx.cond(
                DocuState.is_sidebar_open,
                "fixed inset-y-0 left-0 w-72 bg-white z-[60] shadow-2xl transition-transform duration-300 translate-x-0",
                "fixed inset-y-0 left-0 w-72 bg-white z-[60] shadow-2xl transition-transform duration-300 -translate-x-full",
            ),
        ),
    )