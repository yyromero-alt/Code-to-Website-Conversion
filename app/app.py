import reflex as rx
from app.states.docu_state import DocuState
from app.components.sidebar import sidebar, mobile_sidebar
from app.components.document_view import document_view
from app.components.shipment_views import (
    tracking_list_view,
    tracking_detail_view,
    new_shipment_form_view,
)
from app.components.admin_view import admin_view
from app.components.inventory_view import inventory_view
from app.states.auth_state import AuthState
from app.states.inventory_state import InventoryState
from app.pages.login import login_page


def mobile_header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.icon("truck", class_name="w-5 h-5 text-white"),
                class_name="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center",
            ),
            rx.el.h1(
                "Trazo", class_name="font-bold text-lg italic text-slate-900"
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.button(
            rx.icon("menu", class_name="w-6 h-6"),
            on_click=DocuState.toggle_sidebar,
            class_name="p-2 hover:bg-slate-100 rounded-lg",
        ),
        class_name="lg:hidden bg-white border-b border-slate-200 p-4 flex items-center justify-between sticky top-0 z-40",
    )


def index() -> rx.Component:
    return rx.el.div(
        mobile_sidebar(),
        sidebar(),
        rx.el.div(
            mobile_header(),
            rx.el.main(
                rx.match(
                    DocuState.active_tab,
                    ("documentos", document_view()),
                    ("envios", new_shipment_form_view()),
                    ("seguimiento_v1", tracking_list_view()),
                    ("seguimiento_v2", tracking_detail_view()),
                    ("admin", admin_view()),
                    ("inventarios", inventory_view()),
                    document_view(),
                ),
                class_name="flex-1 p-4 md:p-8 lg:p-12 max-w-7xl mx-auto w-full",
            ),
            class_name="flex-1 flex flex-col min-w-0 bg-slate-50",
        ),
        class_name="min-h-screen flex font-['Inter'] text-slate-900",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(
    index,
    route="/",
    on_load=[
        AuthState.check_auth_status,
        DocuState.load_shared_data,
        InventoryState.load_inventory_data,
    ],
)
app.add_page(login_page, route="/login", on_load=AuthState.check_login_page)