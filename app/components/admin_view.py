import reflex as rx
from app.states.docu_state import DocuState
from app.states.auth_state import AuthState


def stat_card(
    label: str, value: rx.Var[int], icon_name: str, color_class: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                icon_name,
                class_name=f"w-6 h-6 {color_class.replace('bg-', 'text-')}",
            ),
            class_name=f"w-12 h-12 rounded-xl {color_class} flex items-center justify-center mb-4",
        ),
        rx.el.p(
            value.to_string(),
            class_name="text-3xl font-extrabold text-slate-900",
        ),
        rx.el.p(label, class_name="text-sm text-slate-500 font-medium"),
        class_name="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm",
    )


def category_row(cat: dict) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            cat["name"].to(str), class_name="font-medium text-slate-700"
        ),
        rx.el.span(
            cat["count"].to(str),
            class_name="bg-slate-100 text-slate-500 px-2.5 py-0.5 rounded-full text-xs font-bold",
        ),
        class_name="flex items-center justify-between py-3 border-b border-slate-50 last:border-0",
    )


def activity_row(doc: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(class_name="w-2 h-2 rounded-full bg-blue-500 flex-shrink-0"),
        rx.el.div(
            rx.el.p(
                doc["name"].to(str),
                class_name="font-bold text-sm text-slate-900 truncate",
            ),
            rx.el.p(doc["date"].to(str), class_name="text-xs text-slate-400"),
            class_name="flex-1 min-w-0",
        ),
        rx.el.span(
            doc["category"].to(str),
            class_name="px-2 py-0.5 bg-blue-50 text-blue-600 rounded text-[10px] font-bold uppercase",
        ),
        class_name="flex items-center gap-4 py-3 border-b border-slate-50 last:border-0",
    )


def user_row(user: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    user["username"].to(str),
                    class_name="font-bold text-sm text-slate-900",
                ),
                rx.el.p(
                    user["created_at"].to(str)[:10],
                    class_name="text-xs text-slate-400",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.span(
                    user["role"].to(str),
                    class_name=rx.cond(
                        user["role"] == "admin",
                        "bg-blue-50 text-blue-600 px-2 py-0.5 rounded text-[10px] font-bold uppercase",
                        "bg-slate-100 text-slate-500 px-2 py-0.5 rounded text-[10px] font-bold uppercase",
                    ),
                ),
                class_name="flex-1 text-center",
            ),
            rx.el.div(
                rx.cond(
                    user["username"] != AuthState.current_user,
                    rx.el.button(
                        rx.icon("trash-2", class_name="w-4 h-4"),
                        on_click=lambda: AuthState.delete_user(
                            user["username"].to(str)
                        ),
                        class_name="p-2 text-slate-300 hover:text-red-500 hover:bg-red-50 rounded-xl transition-all",
                    ),
                ),
                class_name="flex-1 flex justify-end",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        class_name="py-4 border-b border-slate-100 flex items-center justify-between last:border-0",
    )


def admin_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Administración",
                class_name="text-3xl font-extrabold text-slate-900 tracking-tight",
            ),
            rx.el.p(
                "Gestión del sistema y configuraciones.",
                class_name="text-slate-500 mt-1",
            ),
            class_name="mb-8",
        ),
        rx.el.div(
            stat_card(
                "Total Documentos",
                DocuState.total_documents,
                "file-text",
                "bg-blue-50",
            ),
            stat_card(
                "Envíos Activos",
                DocuState.active_shipments,
                "truck",
                "bg-amber-50",
            ),
            stat_card(
                "Entregados",
                DocuState.delivered_shipments,
                "circle-check",
                "bg-green-50",
            ),
            stat_card(
                "Categorías",
                DocuState.unique_categories.length(),
                "folder",
                "bg-purple-50",
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("users", class_name="w-5 h-5 text-slate-400"),
                rx.el.h3(
                    "Gestión de Usuarios",
                    class_name="text-lg font-bold text-slate-900",
                ),
                rx.el.span(
                    "Administra los usuarios del sistema",
                    class_name="text-sm text-slate-500 font-medium ml-2",
                ),
                class_name="flex items-center gap-2 mb-6",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("plus", class_name="w-4 h-4"),
                    rx.el.span("Nuevo Usuario"),
                    on_click=AuthState.toggle_create_user_form,
                    class_name="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl text-sm font-bold transition-colors mb-6",
                ),
                rx.cond(
                    AuthState.show_create_user_form,
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Usuario",
                                class_name="block text-xs font-bold text-slate-500 uppercase mb-1",
                            ),
                            rx.el.input(
                                placeholder="Nombre de usuario",
                                on_change=AuthState.set_new_user_username,
                                class_name="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-100 outline-none",
                                default_value=AuthState.new_user_username,
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Contraseña",
                                class_name="block text-xs font-bold text-slate-500 uppercase mb-1",
                            ),
                            rx.el.input(
                                type="password",
                                placeholder="••••••••",
                                on_change=AuthState.set_new_user_password,
                                class_name="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-100 outline-none",
                                default_value=AuthState.new_user_password,
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Rol",
                                class_name="block text-xs font-bold text-slate-500 uppercase mb-1",
                            ),
                            rx.el.select(
                                rx.el.option("Administrador", value="admin"),
                                rx.el.option("Visualizador", value="viewer"),
                                on_change=AuthState.set_new_user_role,
                                value=AuthState.new_user_role,
                                class_name="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-100 outline-none appearance-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Cancelar",
                                on_click=AuthState.toggle_create_user_form,
                                class_name="px-4 py-2 text-slate-500 hover:bg-slate-100 rounded-lg text-sm font-bold transition-colors",
                            ),
                            rx.el.button(
                                "Crear Usuario",
                                on_click=AuthState.create_user,
                                class_name="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-bold transition-colors",
                            ),
                            class_name="flex items-center gap-2 pt-5",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-4 gap-4 items-start bg-slate-50 p-4 rounded-2xl border border-slate-200 mb-6",
                    ),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            "Usuario",
                            class_name="flex-1 text-xs font-bold text-slate-400 uppercase tracking-wider",
                        ),
                        rx.el.div(
                            "Rol",
                            class_name="flex-1 text-center text-xs font-bold text-slate-400 uppercase tracking-wider",
                        ),
                        rx.el.div(
                            "Acciones",
                            class_name="flex-1 text-right text-xs font-bold text-slate-400 uppercase tracking-wider",
                        ),
                        class_name="flex items-center justify-between pb-3 border-b border-slate-200",
                    ),
                    rx.foreach(AuthState.users_list, user_row),
                ),
            ),
            class_name="bg-white rounded-[2rem] border border-slate-200 p-8 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("folder", class_name="w-5 h-5 text-slate-400"),
                    rx.el.h3(
                        "Categorías de Documentos",
                        class_name="text-lg font-bold",
                    ),
                    class_name="flex items-center gap-3 mb-6",
                ),
                rx.el.div(
                    rx.foreach(DocuState.unique_categories, category_row),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.input(
                        placeholder="Nueva categoría...",
                        on_change=DocuState.set_new_category_input,
                        class_name="flex-1 px-4 py-2 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-100 outline-none",
                        default_value=DocuState.new_category_input,
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="w-4 h-4"),
                        on_click=DocuState.add_custom_category,
                        class_name="p-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors",
                    ),
                    class_name="flex gap-2",
                ),
                class_name="bg-white rounded-[2rem] border border-slate-200 p-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("activity", class_name="w-5 h-5 text-slate-400"),
                    rx.el.h3(
                        "Actividad Reciente", class_name="text-lg font-bold"
                    ),
                    class_name="flex items-center gap-3 mb-6",
                ),
                rx.el.div(rx.foreach(DocuState.recent_documents, activity_row)),
                class_name="bg-white rounded-[2rem] border border-slate-200 p-8",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8",
        ),
        rx.el.div(
            rx.el.h3(
                "Información del Sistema", class_name="text-lg font-bold mb-4"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Versión App",
                        class_name="text-xs text-slate-400 font-bold uppercase tracking-wider mb-1",
                    ),
                    rx.el.p(
                        "Trazo v1.0", class_name="font-bold text-slate-700"
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        "Envíos Totales",
                        class_name="text-xs text-slate-400 font-bold uppercase tracking-wider mb-1",
                    ),
                    rx.el.p(
                        DocuState.shipments.length().to_string(),
                        class_name="font-bold text-slate-700",
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        "Almacenamiento",
                        class_name="text-xs text-slate-400 font-bold uppercase tracking-wider mb-1",
                    ),
                    rx.el.p(
                        "Simulado (Local)",
                        class_name="font-bold text-slate-700",
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-8",
            ),
            class_name="bg-white rounded-[2rem] border border-slate-200 p-8",
        ),
        class_name="animate-in fade-in duration-500",
    )


def admin_view() -> rx.Component:
    return rx.cond(
        AuthState.is_admin,
        admin_content(),
        rx.el.div(
            rx.icon("shield-alert", class_name="w-12 h-12 text-red-500 mb-4"),
            rx.el.h2(
                "Acceso Restringido",
                class_name="text-2xl font-bold text-slate-900",
            ),
            rx.el.p(
                "No tienes permisos para acceder a la administración.",
                class_name="text-slate-500 font-medium",
            ),
            class_name="flex flex-col items-center justify-center p-20 bg-white rounded-[2rem] border border-slate-200",
        ),
    )