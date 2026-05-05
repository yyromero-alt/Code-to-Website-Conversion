import reflex as rx
from app.states.inventory_state import InventoryState
from app.states.auth_state import AuthState


def status_dot(color: str, label: str, count: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(class_name=f"w-3 h-3 rounded-full {color}"),
        rx.el.span(
            label, class_name="text-sm font-medium text-slate-700 flex-1"
        ),
        rx.el.span(count, class_name="font-bold text-sm text-slate-900"),
        class_name="flex items-center gap-3 py-2",
    )


def inventory_item_row(item: dict) -> rx.Component:
    estado_color = rx.match(
        item["estado"],
        ("Coincide", "bg-green-50 text-green-600"),
        ("Sobrante", "bg-amber-50 text-amber-600"),
        ("Faltante", "bg-red-50 text-red-600"),
        "bg-slate-50 text-slate-500",
    )
    row_color = rx.match(
        item["estado"],
        ("Coincide", "hover:bg-green-50/30"),
        ("Sobrante", "hover:bg-amber-50/30"),
        ("Faltante", "hover:bg-red-50/30"),
        "hover:bg-slate-50/50",
    )
    diff_color = rx.match(
        item["estado"],
        ("Coincide", "text-green-600"),
        ("Sobrante", "text-amber-600"),
        ("Faltante", "text-red-600"),
        "text-slate-600",
    )
    return rx.el.tr(
        rx.el.td(
            item["product_code"].to(str),
            class_name="py-3 px-4 text-sm font-bold text-slate-900",
        ),
        rx.el.td(
            item["stock_latin"].to(str),
            class_name="py-3 px-4 text-sm text-slate-600 text-center",
        ),
        rx.el.td(
            item["stock_imc"].to(str),
            class_name="py-3 px-4 text-sm text-slate-600 text-center",
        ),
        rx.el.td(
            item["diferencia"].to(str),
            class_name=f"py-3 px-4 text-sm font-bold {diff_color} text-center",
        ),
        rx.el.td(
            rx.el.span(
                item["estado"].to(str),
                class_name=f"{estado_color} px-2.5 py-1 rounded-md text-[11px] font-bold uppercase",
            ),
            class_name="py-3 px-4",
        ),
        rx.el.td(
            rx.cond(
                item["observacion"] != "",
                rx.el.span(
                    item["observacion"].to(str),
                    class_name=rx.match(
                        item["observacion"].to(str),
                        (
                            "Solo en IMC",
                            "bg-purple-100 text-purple-700 px-2 py-1 rounded-md text-[10px] font-bold uppercase",
                        ),
                        (
                            "Solo en LATIN",
                            "bg-indigo-100 text-indigo-700 px-2 py-1 rounded-md text-[10px] font-bold uppercase",
                        ),
                        "text-slate-500",
                    ),
                ),
                rx.el.span(),
            ),
            class_name="py-3 px-4 text-xs max-w-[200px] truncate",
        ),
        rx.el.td(
            rx.cond(
                AuthState.is_admin,
                rx.el.button(
                    rx.icon("trash-2", class_name="w-4 h-4"),
                    on_click=lambda: InventoryState.delete_inventory_item(
                        item["item_id"].to(str)
                    ),
                    class_name="p-2 text-slate-300 hover:text-red-500 hover:bg-red-50 rounded-xl transition-all",
                ),
            ),
            class_name="py-3 px-4 text-right",
        ),
        class_name=f"border-b border-slate-50 last:border-0 transition-colors {row_color}",
    )


def source_summary_card(
    title: str, value: rx.Var, icon_name: str, color_class: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                icon_name,
                class_name=f"w-5 h-5 {color_class.replace('bg-', 'text-')}",
            ),
            class_name=f"w-10 h-10 rounded-xl {color_class} flex items-center justify-center",
        ),
        rx.el.div(
            rx.el.p(
                title,
                class_name="text-xs text-slate-500 font-bold uppercase tracking-wider mb-1",
            ),
            rx.el.p(value, class_name="text-2xl font-extrabold text-slate-900"),
        ),
        class_name="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm flex items-center gap-4",
    )


def inventory_dashboard_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Cruce de Inventarios",
                    class_name="text-3xl font-extrabold text-slate-900 tracking-tight",
                ),
                rx.el.p(
                    "Compara stock LATIN vs IMC e identifica discrepancias.",
                    class_name="text-slate-500 mt-1",
                ),
            ),
            rx.cond(
                InventoryState.inventory_items.length() > 0,
                rx.el.button(
                    rx.icon("download", class_name="w-4 h-4 mr-2"),
                    "Descargar Reporte",
                    on_click=InventoryState.download_report,
                    class_name="flex items-center px-4 py-2 bg-white border border-slate-200 rounded-xl text-blue-600 font-bold hover:bg-slate-50 transition-colors shadow-sm",
                ),
            ),
            class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6",
        ),
        rx.el.div(
            source_summary_card(
                "Inventario IMC (Cliente)",
                rx.cond(
                    InventoryState.imc_total_rows > 0,
                    rx.cond(
                        InventoryState.imc_total_rows > 0,
                        InventoryState.imc_total_rows.to_string()
                        + " filas ("
                        + InventoryState.imc_unique_refs.to_string()
                        + " refs)",
                        "0 filas (0 refs)",
                    ),
                    InventoryState.imc_total_rows.to_string(),
                ),
                "warehouse",
                "bg-purple-50",
            ),
            source_summary_card(
                "Inventario LATIN (Empresa)",
                rx.cond(
                    InventoryState.latin_total_products > 0,
                    rx.cond(
                        InventoryState.latin_total_products > 0,
                        InventoryState.latin_total_products.to_string()
                        + " productos",
                        "0 productos",
                    ),
                    InventoryState.latin_total_products.to_string(),
                ),
                "building-2",
                "bg-indigo-50",
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "clipboard-list", class_name="w-6 h-6 text-blue-600"
                    ),
                    class_name="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center mb-4",
                ),
                rx.el.p(
                    InventoryState.total_items.to_string(),
                    class_name="text-3xl font-extrabold text-slate-900",
                ),
                rx.el.p(
                    "Total Productos",
                    class_name="text-sm text-slate-500 font-medium",
                ),
                class_name="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("smile", class_name="w-6 h-6 text-green-600"),
                    class_name="w-12 h-12 rounded-xl bg-green-50 flex items-center justify-center mb-4",
                ),
                rx.el.p(
                    InventoryState.matched_count.to_string(),
                    class_name="text-3xl font-extrabold text-slate-900",
                ),
                rx.el.p(
                    "Coincidencias",
                    class_name="text-sm text-slate-500 font-medium",
                ),
                class_name="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("skull", class_name="w-6 h-6 text-red-600"),
                    class_name="w-12 h-12 rounded-xl bg-red-50 flex items-center justify-center mb-4",
                ),
                rx.el.p(
                    InventoryState.discrepancy_count.to_string(),
                    class_name="text-3xl font-extrabold text-slate-900",
                ),
                rx.el.p(
                    "Discrepancias",
                    class_name="text-sm text-slate-500 font-medium",
                ),
                rx.el.p(
                    "Click para ver detalles",
                    class_name="text-[10px] text-red-500 font-bold mt-2 uppercase tracking-tight",
                ),
                on_click=InventoryState.toggle_discrepancies,
                class_name="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm cursor-pointer hover:shadow-md hover:scale-[1.02] transition-all",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("target", class_name="w-6 h-6 text-purple-600"),
                    class_name="w-12 h-12 rounded-xl bg-purple-50 flex items-center justify-center mb-4",
                ),
                rx.el.p(
                    f"{InventoryState.accuracy_pct:.1f}%",
                    class_name="text-3xl font-extrabold text-slate-900",
                ),
                rx.el.p(
                    "Precisión %",
                    class_name="text-sm text-slate-500 font-medium",
                ),
                class_name="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm",
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8",
        ),
        rx.cond(
            InventoryState.show_discrepancies,
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.icon("skull", class_name="w-6 h-6 text-red-600"),
                            rx.el.h3(
                                "Referencias con Discrepancias",
                                class_name="text-lg font-bold text-slate-900",
                            ),
                            rx.el.span(
                                InventoryState.discrepancy_count.to_string(),
                                class_name="bg-red-100 text-red-600 px-2 py-0.5 rounded-full text-xs font-bold",
                            ),
                            class_name="flex items-center gap-3",
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="w-5 h-5"),
                            on_click=InventoryState.toggle_discrepancies,
                            class_name="p-2 hover:bg-slate-100 rounded-lg text-slate-400 transition-colors",
                        ),
                        class_name="flex justify-between items-center mb-6",
                    ),
                    rx.cond(
                        InventoryState.discrepancy_items.length() > 0,
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th(
                                            "CÓDIGO",
                                            class_name="text-left py-3 px-4 text-xs font-bold text-slate-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "STOCK LATIN",
                                            class_name="text-center py-3 px-4 text-xs font-bold text-slate-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "STOCK IMC",
                                            class_name="text-center py-3 px-4 text-xs font-bold text-slate-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "DIFERENCIA",
                                            class_name="text-center py-3 px-4 text-xs font-bold text-slate-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "ESTADO",
                                            class_name="text-left py-3 px-4 text-xs font-bold text-slate-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "OBSERVACIÓN",
                                            class_name="text-left py-3 px-4 text-xs font-bold text-slate-500 uppercase tracking-wider",
                                        ),
                                        class_name="bg-slate-50",
                                    )
                                ),
                                rx.el.tbody(
                                    rx.foreach(
                                        InventoryState.discrepancy_items,
                                        inventory_item_row,
                                    )
                                ),
                                class_name="w-full text-left border-collapse",
                            ),
                            class_name="overflow-x-auto",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "No hay discrepancias 🎉",
                                class_name="text-green-600 font-bold text-lg",
                            ),
                            class_name="p-12 text-center",
                        ),
                    ),
                    class_name="bg-white rounded-2xl border border-slate-200 border-l-4 border-l-red-500 p-8 shadow-sm",
                ),
                class_name="animate-in slide-in-from-top-4 duration-300 mb-8",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Distribución por Estado",
                    class_name="font-bold text-lg text-slate-900 mb-6",
                ),
                rx.recharts.pie_chart(
                    rx.recharts.graphing_tooltip(separator=""),
                    rx.recharts.pie(
                        data=InventoryState.status_chart_data,
                        data_key="value",
                        name_key="name",
                        cx="50%",
                        cy="50%",
                        inner_radius="60%",
                        outer_radius="80%",
                        stroke="#ffffff",
                        stroke_width=2,
                    ),
                    height=250,
                    width="100%",
                ),
                class_name="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm",
            ),
            rx.el.div(
                rx.el.h3(
                    "Resumen de Cruce",
                    class_name="font-bold text-lg text-slate-900 mb-6",
                ),
                rx.el.div(
                    status_dot(
                        "bg-green-500",
                        "Coinciden (Diferencia = 0)",
                        InventoryState.matched_count.to_string(),
                    ),
                    rx.el.div(class_name="h-px bg-slate-100 my-2"),
                    status_dot(
                        "bg-amber-500",
                        "Sobrantes (LATIN > IMC)",
                        InventoryState.status_chart_data[1][
                            "value"
                        ].to_string(),
                    ),
                    rx.el.div(class_name="h-px bg-slate-100 my-2"),
                    status_dot(
                        "bg-red-500",
                        "Faltantes (LATIN < IMC)",
                        InventoryState.status_chart_data[2][
                            "value"
                        ].to_string(),
                    ),
                    class_name="flex flex-col",
                ),
                class_name="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col justify-center",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8",
        ),
        rx.cond(
            AuthState.is_admin,
            rx.el.div(
                rx.el.div(
                    rx.icon("cloud-upload", class_name="w-8 h-8 text-blue-600"),
                    class_name="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mb-6",
                ),
                rx.el.h3(
                    "Importar Cruce de Inventario",
                    class_name="font-bold text-lg text-slate-900 mb-2",
                ),
                rx.el.p(
                    "Sube tu archivo Excel (.xlsx) con el cruce LATIN vs IMC",
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
                    id="inventory_excel",
                    accept={
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
                            ".xlsx"
                        ],
                        "application/vnd.ms-excel": [".xls"],
                    },
                    multiple=False,
                    on_drop=InventoryState.handle_inventory_excel_upload(
                        rx.upload_files(upload_id="inventory_excel")
                    ),
                ),
                rx.cond(
                    InventoryState.import_message != "",
                    rx.el.div(
                        rx.icon("info", class_name="w-5 h-5 text-blue-600"),
                        rx.el.span(
                            InventoryState.import_message,
                            class_name="font-medium text-blue-900",
                        ),
                        class_name="mt-4 p-4 bg-blue-50 rounded-xl border border-blue-100 flex items-center gap-3",
                    ),
                ),
                class_name="bg-white rounded-[2rem] border border-slate-200 p-8 shadow-sm mb-8",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("search", class_name="w-5 h-5 text-slate-400"),
                    rx.el.input(
                        placeholder="Buscar código...",
                        on_change=InventoryState.set_inventory_search.debounce(
                            500
                        ),
                        class_name="flex-1 bg-transparent outline-none text-sm",
                        default_value=InventoryState.inventory_search,
                    ),
                    class_name="flex-1 flex items-center gap-2 px-4 py-2 border border-slate-200 rounded-xl focus-within:ring-2 focus-within:ring-blue-100 bg-white",
                ),
                rx.el.select(
                    rx.el.option("Todos", value="all"),
                    rx.el.option("Coincide", value="match"),
                    rx.el.option("Sobrante", value="sobrante"),
                    rx.el.option("Faltante", value="faltante"),
                    on_change=InventoryState.set_inventory_filter,
                    value=InventoryState.inventory_filter,
                    class_name="px-4 py-2 border border-slate-200 rounded-xl text-sm bg-white outline-none focus:ring-2 focus:ring-blue-100 appearance-none",
                ),
                class_name="flex items-center gap-4 mb-6",
            ),
            rx.el.div(
                rx.cond(
                    InventoryState.filtered_items.length() > 0,
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "CÓDIGO",
                                    class_name="text-left py-3 px-4 text-xs font-bold text-slate-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "STOCK LATIN",
                                    class_name="text-center py-3 px-4 text-xs font-bold text-slate-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "STOCK IMC",
                                    class_name="text-center py-3 px-4 text-xs font-bold text-slate-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "DIFERENCIA",
                                    class_name="text-center py-3 px-4 text-xs font-bold text-slate-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "ESTADO",
                                    class_name="text-left py-3 px-4 text-xs font-bold text-slate-500 uppercase tracking-wider",
                                ),
                                rx.el.th(
                                    "OBSERVACIÓN",
                                    class_name="text-left py-3 px-4 text-xs font-bold text-slate-500 uppercase tracking-wider",
                                ),
                                rx.el.th("", class_name="py-3 px-4"),
                                class_name="bg-slate-50",
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                InventoryState.filtered_items,
                                inventory_item_row,
                            )
                        ),
                        class_name="w-full text-left border-collapse",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "No se encontraron productos.",
                            class_name="text-slate-500 font-medium",
                        ),
                        class_name="p-12 text-center",
                    ),
                ),
                class_name="overflow-x-auto",
            ),
            class_name="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm",
        ),
        class_name="animate-in fade-in duration-500",
    )


def audit_card(audit: dict) -> rx.Component:
    accuracy = audit["accuracy"].to(float)
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    audit["date"].to(str),
                    class_name="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1",
                ),
                rx.el.h3(
                    f"Precisión: {accuracy:.1f}%",
                    class_name="text-xl font-bold text-slate-900",
                ),
            ),
            rx.el.span(
                rx.cond(accuracy == 100, "Perfecta", "Con Discrepancias"),
                class_name=rx.cond(
                    accuracy == 100,
                    "bg-green-50 text-green-600 px-3 py-1 rounded-lg text-xs font-bold",
                    "bg-amber-50 text-amber-600 px-3 py-1 rounded-lg text-xs font-bold",
                ),
            ),
            class_name="flex items-start justify-between mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Total Ítems",
                    class_name="text-[10px] uppercase text-slate-400 font-bold mb-1",
                ),
                rx.el.p(
                    audit["total_items"].to(str),
                    class_name="font-bold text-slate-700",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Coinciden",
                    class_name="text-[10px] uppercase text-slate-400 font-bold mb-1",
                ),
                rx.el.p(
                    audit["matched"].to(str),
                    class_name="font-bold text-green-600",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    "Discrepan",
                    class_name="text-[10px] uppercase text-slate-400 font-bold mb-1",
                ),
                rx.el.p(
                    audit["discrepancies"].to(str),
                    class_name="font-bold text-red-600",
                ),
            ),
            class_name="grid grid-cols-3 gap-4 pb-4 border-b border-slate-100",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Generado por:", class_name="text-xs text-slate-500 mr-2"
                ),
                rx.el.span(
                    audit["created_by"].to(str),
                    class_name="text-xs font-bold text-slate-700",
                ),
                class_name="flex items-center",
            ),
            rx.cond(
                AuthState.is_admin,
                rx.el.button(
                    rx.icon("trash-2", class_name="w-4 h-4"),
                    on_click=lambda: InventoryState.delete_audit(
                        audit["audit_id"].to(str)
                    ),
                    class_name="p-2 text-slate-300 hover:text-red-500 hover:bg-red-50 rounded-xl transition-colors",
                ),
            ),
            class_name="pt-4 flex items-center justify-between",
        ),
        class_name="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm",
    )


def inventory_audits_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Historial de Auditorías",
                    class_name="text-3xl font-extrabold text-slate-900 tracking-tight",
                ),
                rx.el.p(
                    "Registros históricos de precisión de inventarios.",
                    class_name="text-slate-500 mt-1",
                ),
            ),
            rx.cond(
                AuthState.is_admin,
                rx.el.button(
                    rx.icon("plus", class_name="w-4 h-4"),
                    rx.el.span("Ejecutar Nueva Auditoría"),
                    on_click=InventoryState.run_audit,
                    class_name="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-bold shadow-lg transition-colors",
                ),
            ),
            class_name="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8",
        ),
        rx.cond(
            InventoryState.inventory_audits.length() > 0,
            rx.el.div(
                rx.foreach(InventoryState.inventory_audits, audit_card),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
            ),
            rx.el.div(
                rx.icon(
                    "clipboard-list", class_name="w-12 h-12 text-slate-200 mb-4"
                ),
                rx.el.p(
                    "No hay auditorías registradas.",
                    class_name="text-slate-500 font-medium",
                ),
                class_name="flex flex-col items-center justify-center p-20 bg-white rounded-[2rem] border border-slate-200",
            ),
        ),
        class_name="animate-in fade-in duration-500",
    )


def inventory_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                "Dashboard",
                on_click=lambda: InventoryState.set_inventory_tab("dashboard"),
                class_name=rx.cond(
                    InventoryState.active_inventory_tab == "dashboard",
                    "px-6 py-2 rounded-xl text-sm font-bold bg-blue-600 text-white shadow-md",
                    "px-6 py-2 rounded-xl text-sm font-bold text-slate-500 hover:bg-slate-100",
                ),
            ),
            rx.el.button(
                "Auditorías",
                on_click=lambda: InventoryState.set_inventory_tab("audits"),
                class_name=rx.cond(
                    InventoryState.active_inventory_tab == "audits",
                    "px-6 py-2 rounded-xl text-sm font-bold bg-blue-600 text-white shadow-md",
                    "px-6 py-2 rounded-xl text-sm font-bold text-slate-500 hover:bg-slate-100",
                ),
            ),
            class_name="flex items-center gap-2 p-1 bg-white border border-slate-200 rounded-2xl w-fit mb-8",
        ),
        rx.cond(
            InventoryState.active_inventory_tab == "dashboard",
            inventory_dashboard_view(),
            inventory_audits_view(),
        ),
        class_name="w-full",
    )