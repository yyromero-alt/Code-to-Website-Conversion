import reflex as rx
from app.states.docu_state import DocuState
from app.states.auth_state import AuthState


def tracking_list_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Panel de Control",
                class_name="text-3xl font-extrabold text-slate-900 tracking-tight",
            ),
            rx.el.p(
                "Resumen general de envíos y logística.",
                class_name="text-slate-500 mt-1",
            ),
            class_name="mb-8",
        ),
        rx.cond(
            DocuState.total_shipments_count > 0,
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "package", class_name="w-6 h-6 text-blue-600"
                            ),
                            class_name="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center mb-4",
                        ),
                        rx.el.p(
                            DocuState.total_shipments_count.to_string(),
                            class_name="text-3xl font-extrabold text-slate-900",
                        ),
                        rx.el.p(
                            "Total Envíos",
                            class_name="text-sm text-slate-500 font-medium",
                        ),
                        rx.el.p(
                            f"unidades: {DocuState.total_units}",
                            class_name="text-xs text-slate-400 mt-2",
                        ),
                        class_name="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "circle-check",
                                class_name="w-6 h-6 text-green-600",
                            ),
                            class_name="w-12 h-12 rounded-xl bg-green-50 flex items-center justify-center mb-4",
                        ),
                        rx.el.p(
                            DocuState.delivered_shipments.to_string(),
                            class_name="text-3xl font-extrabold text-green-600",
                        ),
                        rx.el.p(
                            "Entregados",
                            class_name="text-sm text-slate-500 font-medium",
                        ),
                        rx.el.div(
                            rx.el.div(
                                class_name="bg-green-500 h-full rounded-full",
                                style={
                                    "width": f"{DocuState.delivered_percentage}%"
                                },
                            ),
                            class_name="w-full h-1.5 bg-green-100 rounded-full mt-3",
                        ),
                        class_name="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "truck", class_name="w-6 h-6 text-blue-600"
                            ),
                            class_name="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center mb-4",
                        ),
                        rx.el.p(
                            DocuState.active_shipments.to_string(),
                            class_name="text-3xl font-extrabold text-blue-600",
                        ),
                        rx.el.p(
                            "En Tránsito",
                            class_name="text-sm text-slate-500 font-medium",
                        ),
                        rx.el.div(
                            rx.el.div(
                                class_name="bg-blue-500 h-full rounded-full",
                                style={
                                    "width": f"{DocuState.in_transit_percentage}%"
                                },
                            ),
                            class_name="w-full h-1.5 bg-blue-100 rounded-full mt-3",
                        ),
                        class_name="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "dollar-sign",
                                class_name="w-6 h-6 text-amber-600",
                            ),
                            class_name="w-12 h-12 rounded-xl bg-amber-50 flex items-center justify-center mb-4",
                        ),
                        rx.el.p(
                            f"${DocuState.total_value:,.2f}",
                            class_name="text-3xl font-extrabold text-slate-900 truncate",
                        ),
                        rx.el.p(
                            "Valoración Total",
                            class_name="text-sm text-slate-500 font-medium",
                        ),
                        class_name="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm",
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mt-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "pie-chart",
                                class_name="w-5 h-5 text-slate-400 mr-2",
                            ),
                            rx.el.h3(
                                "Distribución por Estado",
                                class_name="font-bold text-lg text-slate-900",
                            ),
                            class_name="flex items-center mb-6",
                        ),
                        rx.recharts.responsive_container(
                            rx.recharts.pie_chart(
                                rx.recharts.graphing_tooltip(),
                                rx.recharts.pie(
                                    data=DocuState.status_chart_data,
                                    data_key="value",
                                    name_key="name",
                                    cx="50%",
                                    cy="50%",
                                    inner_radius="60%",
                                    outer_radius="80%",
                                    fill="#8884d8",
                                    stroke="#ffffff",
                                    stroke_width=2,
                                ),
                            ),
                            width="100%",
                            height=300,
                        ),
                        class_name="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "bar-chart-3",
                                class_name="w-5 h-5 text-slate-400 mr-2",
                            ),
                            rx.el.h3(
                                "Envíos por Mes",
                                class_name="font-bold text-lg text-slate-900",
                            ),
                            class_name="flex items-center mb-6",
                        ),
                        rx.recharts.responsive_container(
                            rx.recharts.bar_chart(
                                rx.recharts.cartesian_grid(
                                    stroke_dasharray="3 3", vertical=False
                                ),
                                rx.recharts.graphing_tooltip(),
                                rx.recharts.x_axis(
                                    data_key="mes",
                                    axis_line=False,
                                    tick_line=False,
                                ),
                                rx.recharts.bar(
                                    data_key="total",
                                    fill="#bfdbfe",
                                    name="Total Envíos",
                                    radius=[4, 4, 0, 0],
                                ),
                                rx.recharts.bar(
                                    data_key="entregados",
                                    fill="#22c55e",
                                    name="Entregados",
                                    radius=[4, 4, 0, 0],
                                ),
                                data=DocuState.monthly_chart_data,
                            ),
                            width="100%",
                            height=300,
                        ),
                        class_name="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "map-pin",
                                class_name="w-5 h-5 text-slate-400 mr-2",
                            ),
                            rx.el.h3(
                                "Top Ciudades Origen",
                                class_name="font-bold text-lg text-slate-900",
                            ),
                            class_name="flex items-center mb-6",
                        ),
                        rx.el.div(
                            rx.foreach(
                                DocuState.top_origins,
                                lambda item: rx.el.div(
                                    rx.el.div(
                                        rx.el.span(
                                            item["city"],
                                            class_name="font-medium text-sm text-slate-700",
                                        ),
                                        rx.el.span(
                                            item["count"],
                                            class_name="bg-blue-50 text-blue-600 px-2.5 py-0.5 rounded-full text-xs font-bold",
                                        ),
                                        class_name="flex justify-between items-center mb-1",
                                    ),
                                    rx.el.div(
                                        rx.el.div(
                                            class_name="bg-blue-100 h-full rounded-full",
                                            style={"width": item["width"]},
                                        ),
                                        class_name="w-full h-2 rounded-full",
                                    ),
                                    class_name="mb-4 last:mb-0",
                                ),
                            )
                        ),
                        class_name="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "map-pin",
                                class_name="w-5 h-5 text-slate-400 mr-2",
                            ),
                            rx.el.h3(
                                "Top Destinos",
                                class_name="font-bold text-lg text-slate-900",
                            ),
                            class_name="flex items-center mb-6",
                        ),
                        rx.el.div(
                            rx.foreach(
                                DocuState.top_destinations,
                                lambda item: rx.el.div(
                                    rx.el.div(
                                        rx.el.span(
                                            item["city"],
                                            class_name="font-medium text-sm text-slate-700",
                                        ),
                                        rx.el.span(
                                            item["count"],
                                            class_name="bg-green-50 text-green-600 px-2.5 py-0.5 rounded-full text-xs font-bold",
                                        ),
                                        class_name="flex justify-between items-center mb-1",
                                    ),
                                    rx.el.div(
                                        rx.el.div(
                                            class_name="bg-green-100 h-full rounded-full",
                                            style={"width": item["width"]},
                                        ),
                                        class_name="w-full h-2 rounded-full",
                                    ),
                                    class_name="mb-4 last:mb-0",
                                ),
                            )
                        ),
                        class_name="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "list", class_name="w-5 h-5 text-slate-400 mr-2"
                        ),
                        rx.el.h3(
                            "Envíos Recientes",
                            class_name="font-bold text-lg text-slate-900",
                        ),
                        class_name="flex items-center p-6 border-b border-slate-200",
                    ),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "GUÍA",
                                        class_name="text-left py-3 px-4 text-xs font-bold text-slate-500 tracking-wider uppercase",
                                    ),
                                    rx.el.th(
                                        "ORIGEN",
                                        class_name="text-left py-3 px-4 text-xs font-bold text-slate-500 tracking-wider uppercase",
                                    ),
                                    rx.el.th(
                                        "DESTINO",
                                        class_name="text-left py-3 px-4 text-xs font-bold text-slate-500 tracking-wider uppercase",
                                    ),
                                    rx.el.th(
                                        "DESTINATARIO",
                                        class_name="text-left py-3 px-4 text-xs font-bold text-slate-500 tracking-wider uppercase",
                                    ),
                                    rx.el.th(
                                        "ESTADO",
                                        class_name="text-left py-3 px-4 text-xs font-bold text-slate-500 tracking-wider uppercase",
                                    ),
                                    rx.el.th(
                                        "VALORACIÓN",
                                        class_name="text-right py-3 px-4 text-xs font-bold text-slate-500 tracking-wider uppercase",
                                    ),
                                    class_name="bg-slate-50",
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    DocuState.recent_shipments_list,
                                    lambda ship: rx.el.tr(
                                        rx.el.td(
                                            ship["guia"],
                                            class_name="py-3 px-4 text-sm font-bold text-slate-900",
                                        ),
                                        rx.el.td(
                                            ship["origin"],
                                            class_name="py-3 px-4 text-sm text-slate-600",
                                        ),
                                        rx.el.td(
                                            ship["destination"],
                                            class_name="py-3 px-4 text-sm text-slate-600",
                                        ),
                                        rx.el.td(
                                            ship["destinatario"],
                                            class_name="py-3 px-4 text-sm text-slate-600",
                                        ),
                                        rx.el.td(
                                            rx.el.span(
                                                ship["status"],
                                                class_name=f"{rx.match(ship['status'], ('Entregado', 'bg-green-50 text-green-600'), ('En camino', 'bg-blue-50 text-blue-600'), ('Pendiente', 'bg-amber-50 text-amber-600'), 'bg-slate-50 text-slate-500')} px-2.5 py-1 rounded-md text-[11px] font-bold uppercase",
                                            ),
                                            class_name="py-3 px-4",
                                        ),
                                        rx.el.td(
                                            rx.cond(
                                                ship["valoracion"] != "",
                                                f"${ship['valoracion']}",
                                                "-",
                                            ),
                                            class_name="py-3 px-4 text-sm font-bold text-slate-900 text-right",
                                        ),
                                        class_name="border-b border-slate-50 last:border-0 hover:bg-slate-50/50 transition-colors",
                                    ),
                                )
                            ),
                            class_name="w-full text-left border-collapse",
                        ),
                        class_name="overflow-x-auto",
                    ),
                    class_name="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm mt-6 mb-8",
                ),
            ),
            rx.el.div(
                rx.icon(
                    "package-search", class_name="w-12 h-12 text-slate-200 mb-4"
                ),
                rx.el.p(
                    "No hay datos de envíos. Importa tus envíos desde la sección Paquetería.",
                    class_name="text-slate-500 font-medium",
                ),
                rx.el.button(
                    "Ir a Paquetería",
                    on_click=lambda: DocuState.set_tab("envios"),
                    class_name="text-blue-600 text-sm font-bold mt-2 hover:underline",
                ),
                class_name="flex flex-col items-center justify-center p-20 bg-white rounded-[2rem] border border-slate-200 mt-8",
            ),
        ),
        class_name="animate-in fade-in duration-500",
    )


def shipment_detail_card(ship: dict) -> rx.Component:
    is_menu_open = DocuState.open_menu_id == ship["id"]
    status_style = rx.match(
        ship["status"],
        ("En camino", "bg-blue-50 text-blue-600"),
        ("Entregado", "bg-green-50 text-green-600"),
        ("Pendiente", "bg-amber-50 text-amber-600"),
        "bg-slate-50 text-slate-500",
    )
    priority_style = rx.match(
        ship["priority"],
        ("Alta", "bg-red-50 text-red-600"),
        ("Normal", "bg-slate-100 text-slate-600"),
        ("Urgente", "bg-red-100 text-red-700"),
        "bg-slate-50 text-slate-500",
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("package", class_name="w-8 h-8"),
                    class_name="p-4 bg-blue-50 text-blue-600 rounded-2xl",
                ),
                rx.el.div(
                    rx.el.span(
                        ship["id"],
                        class_name="text-xs font-black text-slate-400 uppercase tracking-widest",
                    ),
                    rx.el.h3("Carga General", class_name="text-xl font-bold"),
                ),
                class_name="flex gap-4",
            ),
            rx.el.div(
                rx.cond(
                    AuthState.is_admin,
                    rx.el.button(
                        rx.icon("gallery-vertical", class_name="w-6 h-6"),
                        on_click=lambda: DocuState.toggle_shipment_menu(
                            ship["id"]
                        ),
                        class_name="p-2 hover:bg-slate-100 rounded-full text-slate-400",
                    ),
                ),
                rx.cond(
                    is_menu_open,
                    rx.el.div(
                        rx.el.button(
                            rx.el.div(
                                rx.icon(
                                    "trash-2", class_name="w-4 h-4 text-red-500"
                                ),
                                rx.el.span(
                                    "Eliminar Envío", class_name="text-red-500"
                                ),
                                class_name="flex items-center gap-2 px-4 py-2 hover:bg-slate-50 w-full text-left text-sm font-medium",
                            ),
                            on_click=lambda: DocuState.delete_shipment(
                                ship["id"]
                            ),
                        ),
                        class_name="absolute right-0 mt-2 w-48 bg-white border border-slate-200 rounded-xl shadow-xl z-50 overflow-hidden",
                    ),
                ),
                class_name="relative",
            ),
            class_name="flex justify-between items-start mb-8",
        ),
        rx.el.div(
            rx.el.div(ship["origin"], class_name="text-sm font-bold"),
            rx.el.div(
                rx.el.div(
                    class_name="h-full bg-blue-600 transition-all duration-1000",
                    style={"width": f"{ship['progress']}%"},
                ),
                class_name="h-2 bg-slate-100 rounded-full overflow-hidden relative",
            ),
            rx.el.div(
                ship["destination"], class_name="text-sm font-bold text-right"
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-8 items-center",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Estado",
                    class_name="text-[10px] uppercase tracking-widest text-slate-400 mb-1",
                ),
                rx.el.span(
                    ship["status"],
                    class_name=f"{status_style} px-3 py-1 rounded-lg text-xs font-bold",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Prioridad",
                    class_name="text-[10px] uppercase tracking-widest text-slate-400 mb-1",
                ),
                rx.el.span(
                    ship["priority"],
                    class_name=f"{priority_style} px-3 py-1 rounded-lg text-xs font-bold",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Artículos",
                    class_name="text-[10px] uppercase tracking-widest text-slate-400 mb-1",
                ),
                rx.el.div(
                    rx.icon(
                        "package", class_name="w-4 h-4 mr-2 text-slate-400"
                    ),
                    rx.el.span(
                        f"{ship['items']} bultos",
                        class_name="font-bold text-sm text-slate-700",
                    ),
                    class_name="flex items-center",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Fecha Estimada",
                    class_name="text-[10px] uppercase tracking-widest text-slate-400 mb-1",
                ),
                rx.el.div(
                    rx.icon("clock", class_name="w-4 h-4 mr-2 text-slate-400"),
                    rx.el.span(
                        ship["eta"],
                        class_name="font-bold text-sm text-slate-700",
                    ),
                    class_name="flex items-center",
                ),
            ),
            class_name="grid grid-cols-2 md:grid-cols-4 gap-6 mt-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Destinatario",
                    class_name="text-[10px] uppercase tracking-widest text-slate-400 mb-1",
                ),
                rx.el.span(
                    ship["destinatario"],
                    class_name="font-bold text-sm text-slate-700",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Dirección Destino",
                    class_name="text-[10px] uppercase tracking-widest text-slate-400 mb-1",
                ),
                rx.el.span(
                    ship["direccion"],
                    class_name="font-bold text-sm text-slate-700 truncate block max-w-xs",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Valoración",
                    class_name="text-[10px] uppercase tracking-widest text-slate-400 mb-1",
                ),
                rx.el.span(
                    rx.cond(
                        ship["valoracion"] != "",
                        f"${ship['valoracion']}",
                        "N/A",
                    ),
                    class_name="font-bold text-sm text-slate-700",
                ),
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6 pt-6 border-t border-slate-100",
        ),
        class_name="bg-white rounded-[2.5rem] border border-slate-200 shadow-sm p-8",
    )


def tracking_detail_view() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Seguimiento Detallado",
            class_name="text-3xl font-extrabold text-slate-900 tracking-tight",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400",
                ),
                rx.el.input(
                    placeholder="Buscar por número de guía...",
                    on_change=DocuState.set_shipment_search_query.debounce(500),
                    class_name="w-full px-4 py-3 pl-12 bg-white border border-slate-200 rounded-2xl focus:ring-4 focus:ring-blue-100 focus:border-blue-600 outline-none transition-all shadow-sm text-sm font-medium placeholder:text-slate-400",
                    default_value=DocuState.shipment_search_query,
                ),
                rx.cond(
                    DocuState.shipment_search_query != "",
                    rx.el.button(
                        rx.icon("x", class_name="w-4 h-4"),
                        on_click=DocuState.clear_shipment_search,
                        class_name="absolute right-4 top-1/2 -translate-y-1/2 p-1 text-slate-400 hover:text-slate-600",
                    ),
                ),
                class_name="relative",
            ),
            class_name="flex items-center gap-3 mt-4 mb-8",
        ),
        rx.cond(
            DocuState.shipments.length() > 0,
            rx.cond(
                DocuState.filtered_shipments.length() > 0,
                rx.el.div(
                    rx.foreach(
                        DocuState.filtered_shipments, shipment_detail_card
                    ),
                    class_name="grid grid-cols-1 gap-6",
                ),
                rx.el.div(
                    rx.icon(
                        "search-x", class_name="w-12 h-12 text-slate-200 mb-4"
                    ),
                    rx.el.p(
                        "No se encontraron envíos con ese número de guía.",
                        class_name="text-slate-500 font-medium",
                    ),
                    rx.el.button(
                        "Mostrar todos",
                        on_click=DocuState.clear_shipment_search,
                        class_name="text-blue-600 text-sm font-bold mt-2 hover:underline",
                    ),
                    class_name="flex flex-col items-center justify-center p-20 bg-white rounded-[2rem] border border-slate-200",
                ),
            ),
            rx.el.div(
                rx.icon(
                    "package-search", class_name="w-12 h-12 text-slate-200 mb-4"
                ),
                rx.el.p(
                    "No hay envíos para mostrar.",
                    class_name="text-slate-500 font-medium",
                ),
                class_name="flex flex-col items-center justify-center p-20 bg-white rounded-[2rem] border border-slate-200",
            ),
        ),
        class_name="animate-in slide-in-from-bottom-4 duration-500",
    )


def new_shipment_form_view() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Paquetería",
            class_name="text-3xl font-extrabold text-slate-900 tracking-tight",
        ),
        rx.el.p(
            "Importa tus envíos desde un archivo Excel o un enlace de Google Drive.",
            class_name="text-slate-500 mt-1",
        ),
        rx.cond(
            AuthState.is_admin,
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "cloud-upload", class_name="w-8 h-8 text-blue-600"
                        ),
                        class_name="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mb-6",
                    ),
                    rx.el.h3(
                        "Subir Archivo Excel",
                        class_name="font-bold text-lg text-slate-900 mb-2",
                    ),
                    rx.el.p(
                        "Arrastra o selecciona un archivo .xlsx",
                        class_name="text-sm text-slate-500 mb-6",
                    ),
                    rx.upload.root(
                        rx.el.div(
                            rx.icon(
                                "file-spreadsheet",
                                class_name="w-8 h-8 text-slate-400 mb-2",
                            ),
                            rx.el.p(
                                "Seleccionar archivo",
                                class_name="text-sm font-medium text-slate-600",
                            ),
                            class_name="flex flex-col items-center justify-center p-8 border-2 border-dashed border-slate-300 rounded-xl cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-colors",
                        ),
                        id="excel_upload",
                        accept={
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
                                ".xlsx"
                            ],
                            "application/vnd.ms-excel": [".xls"],
                        },
                        multiple=False,
                        on_drop=DocuState.handle_excel_upload(
                            rx.upload_files(upload_id="excel_upload")
                        ),
                    ),
                    class_name="bg-white rounded-[2rem] border border-slate-200 p-8 shadow-sm",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon("link", class_name="w-8 h-8 text-green-600"),
                        class_name="w-16 h-16 bg-green-50 rounded-full flex items-center justify-center mb-6",
                    ),
                    rx.el.h3(
                        "Enlace de Google Drive",
                        class_name="font-bold text-lg text-slate-900 mb-2",
                    ),
                    rx.el.p(
                        "Pega el enlace de tu hoja de cálculo de Google",
                        class_name="text-sm text-slate-500 mb-6",
                    ),
                    rx.el.input(
                        placeholder="https://docs.google.com/spreadsheets/d/...",
                        on_change=DocuState.set_drive_link_input,
                        class_name="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl mb-4 focus:ring-2 focus:ring-green-100 outline-none",
                        default_value=DocuState.drive_link_input,
                    ),
                    rx.el.button(
                        rx.cond(
                            DocuState.is_importing,
                            rx.icon(
                                "loader", class_name="w-5 h-5 animate-spin"
                            ),
                            "Importar",
                        ),
                        on_click=DocuState.import_from_drive,
                        class_name="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl shadow-lg transition-colors flex justify-center items-center gap-2",
                    ),
                    class_name="bg-white rounded-[2rem] border border-slate-200 p-8 shadow-sm",
                ),
                class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8",
            ),
            rx.el.div(
                rx.icon(
                    "shield-alert", class_name="w-12 h-12 text-blue-500 mb-4"
                ),
                rx.el.h3(
                    "Solo los administradores pueden importar datos",
                    class_name="text-xl font-bold text-slate-900",
                ),
                rx.el.p(
                    "Comunícate con un administrador para añadir nuevos envíos al sistema.",
                    class_name="text-slate-500 mt-2 text-center",
                ),
                class_name="flex flex-col items-center justify-center p-20 mt-8 bg-white rounded-[2rem] border border-slate-200 shadow-sm",
            ),
        ),
        rx.cond(
            DocuState.import_message != "",
            rx.el.div(
                rx.icon("info", class_name="w-5 h-5 text-blue-600"),
                rx.el.span(
                    DocuState.import_message,
                    class_name="font-medium text-blue-900",
                ),
                class_name="mt-8 p-4 bg-blue-50 rounded-xl border border-blue-100 flex items-center gap-3",
            ),
        ),
        class_name="animate-in fade-in duration-500",
    )