import reflex as rx
from app.states.docu_state import DocuState
from app.states.auth_state import AuthState


def tag_chip(tag: str) -> rx.Component:
    return rx.el.span(
        tag,
        rx.el.button(
            rx.icon("x", class_name="w-3.5 h-3.5"),
            on_click=lambda: DocuState.remove_tag(tag),
            class_name="hover:text-blue-900",
        ),
        class_name="flex items-center gap-1.5 bg-blue-50 text-blue-700 px-3 py-1.5 rounded-xl text-sm font-bold border border-blue-100",
    )


def document_row(doc: dict) -> rx.Component:
    is_selected = DocuState.selected_docs.contains(doc["id"])
    return rx.el.div(
        rx.el.button(
            rx.cond(
                is_selected,
                rx.icon("square-check", class_name="w-6 h-6 text-blue-600"),
                rx.icon(
                    "square",
                    class_name="w-6 h-6 text-slate-200 group-hover:text-slate-300",
                ),
            ),
            on_click=lambda: DocuState.toggle_doc_selection(doc["id"]),
            class_name="flex-shrink-0",
        ),
        rx.el.div(
            rx.icon("file-text", class_name="w-6 h-6"),
            class_name="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center flex-shrink-0",
        ),
        rx.el.div(
            rx.el.p(
                doc["name"], class_name="font-bold text-slate-900 truncate"
            ),
            rx.el.div(
                rx.el.span(
                    doc["category"],
                    class_name="bg-slate-100 px-2 py-0.5 rounded text-slate-500 uppercase text-[9px] tracking-tighter font-bold",
                ),
                rx.el.span(doc["date"]),
                rx.el.span("•", class_name="hidden sm:inline"),
                rx.el.span(doc["size"], class_name="hidden sm:inline"),
                class_name="flex items-center gap-4 mt-1 text-xs text-slate-400 font-medium",
            ),
            class_name="flex-1 min-w-0",
        ),
        rx.el.button(
            rx.icon("download", class_name="w-5 h-5"),
            on_click=DocuState.download_doc(doc["id"]),
            class_name="p-3 text-slate-300 hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all active:scale-90",
        ),
        rx.cond(
            AuthState.is_admin,
            rx.el.button(
                rx.icon("trash-2", class_name="w-5 h-5"),
                on_click=lambda: DocuState.delete_document(doc["id"]),
                class_name="p-3 text-slate-300 hover:text-red-500 hover:bg-red-50 rounded-xl transition-all active:scale-90",
            ),
        ),
        class_name=rx.cond(
            is_selected,
            "p-4 md:p-6 flex items-center gap-4 transition-all group bg-blue-50/30",
            "p-4 md:p-6 flex items-center gap-4 transition-all group hover:bg-slate-50/80",
        ),
    )


def document_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Gestión de Facturas",
                    class_name="text-3xl font-extrabold text-slate-900 tracking-tight",
                ),
                rx.el.p(
                    "Haz clic en el icono de descarga para obtener tus archivos PDF.",
                    class_name="text-slate-500 mt-1",
                ),
                class_name="flex-1",
            ),
            rx.cond(
                AuthState.is_admin,
                rx.upload.root(
                    rx.el.div(
                        rx.icon(
                            "cloud-upload",
                            class_name="w-5 h-5 group-hover:scale-110 transition-transform",
                        ),
                        rx.el.span("Subir archivos"),
                        class_name="flex items-center justify-center gap-2",
                    ),
                    id="upload_docs",
                    multiple=True,
                    accept={"application/pdf": [".pdf"]},
                    on_drop=DocuState.handle_upload(
                        rx.upload_files(upload_id="upload_docs")
                    ),
                    class_name="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-semibold shadow-lg active:scale-95 group cursor-pointer",
                ),
            ),
            class_name="flex flex-col md:flex-row md:items-center justify-between gap-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("search", class_name="w-5 h-5 text-slate-400 ml-2"),
                rx.foreach(DocuState.search_tags, tag_chip),
                rx.el.input(
                    placeholder=rx.cond(
                        DocuState.search_tags.length() == 0,
                        "Ej: Factura Contrato...",
                        "",
                    ),
                    on_change=DocuState.set_input_value,
                    on_key_down=DocuState.add_search_tag,
                    class_name="flex-1 min-w-[200px] py-2 outline-none bg-transparent text-slate-900 font-medium placeholder:text-slate-400",
                    default_value=DocuState.input_value,
                ),
                rx.cond(
                    (DocuState.search_tags.length() > 0)
                    | (DocuState.input_value != ""),
                    rx.el.button(
                        rx.icon("rotate-ccw", class_name="w-4 h-4"),
                        on_click=DocuState.clear_search,
                        class_name="absolute right-4 p-2 text-slate-300 hover:text-slate-600",
                    ),
                ),
                class_name="min-h-[64px] w-full p-3 bg-white border border-slate-200 rounded-[1.5rem] focus-within:ring-4 focus-within:ring-blue-100 focus-within:border-blue-600 transition-all shadow-sm flex flex-wrap items-center gap-2 pr-12 relative",
            ),
            class_name="mt-8 relative group",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.button(
                        rx.cond(
                            (
                                DocuState.selected_docs.length()
                                == DocuState.filtered_documents.length()
                            )
                            & (DocuState.filtered_documents.length() > 0),
                            rx.icon(
                                "square-check",
                                class_name=rx.cond(
                                    DocuState.selected_docs.length() > 0,
                                    "w-6 h-6 text-blue-400",
                                    "w-6 h-6 text-blue-600",
                                ),
                            ),
                            rx.icon(
                                "square",
                                class_name=rx.cond(
                                    DocuState.selected_docs.length() > 0,
                                    "w-6 h-6 text-slate-700",
                                    "w-6 h-6 text-slate-300",
                                ),
                            ),
                        ),
                        on_click=DocuState.toggle_select_all,
                    ),
                    rx.el.span(
                        rx.cond(
                            DocuState.selected_docs.length() > 0,
                            f"{DocuState.selected_docs.length()} Seleccionados",
                            f"Resultados: {DocuState.filtered_documents.length()}",
                        ),
                        class_name=rx.cond(
                            DocuState.selected_docs.length() > 0,
                            "font-bold text-[11px] uppercase tracking-wider text-slate-300",
                            "font-bold text-[11px] uppercase tracking-wider text-slate-400",
                        ),
                    ),
                    class_name="flex items-center gap-4",
                ),
                rx.cond(
                    DocuState.selected_docs.length() > 0,
                    rx.el.div(
                        rx.el.button(
                            rx.icon("file-down", class_name="w-4 h-4"),
                            rx.el.span("Descargar Selección"),
                            on_click=DocuState.download_selected,
                            class_name="flex items-center gap-2 bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-lg active:scale-95",
                        ),
                        rx.cond(
                            AuthState.is_admin,
                            rx.el.button(
                                rx.icon("trash-2", class_name="w-4 h-4"),
                                rx.el.span("Eliminar Selección"),
                                on_click=DocuState.delete_selected_docs,
                                class_name="flex items-center gap-2 bg-red-600 hover:bg-red-500 px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-lg active:scale-95 text-white",
                            ),
                        ),
                        rx.el.button(
                            rx.icon("x", class_name="w-4 h-4"),
                            on_click=lambda: DocuState.set_selected_docs([]),
                            class_name="p-2 hover:bg-slate-800 rounded-xl",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                ),
                class_name=rx.cond(
                    DocuState.selected_docs.length() > 0,
                    "p-4 md:px-8 py-5 transition-all duration-300 flex flex-col md:flex-row justify-between items-center gap-4 bg-slate-900 text-white",
                    "p-4 md:px-8 py-5 transition-all duration-300 flex flex-col md:flex-row justify-between items-center gap-4 bg-slate-50/50 text-slate-500",
                ),
            ),
            rx.el.div(
                rx.cond(
                    DocuState.filtered_documents.length() > 0,
                    rx.el.div(
                        rx.foreach(DocuState.filtered_documents, document_row),
                        class_name="divide-y divide-slate-100",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "search", class_name="w-8 h-8 text-slate-300"
                            ),
                            class_name="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center mx-auto",
                        ),
                        rx.el.p(
                            "No se encontraron documentos.",
                            class_name="text-slate-500 font-medium mt-4",
                        ),
                        rx.el.button(
                            "Limpiar filtros",
                            on_click=DocuState.clear_search,
                            class_name="text-blue-600 text-sm font-bold hover:underline mt-2",
                        ),
                        class_name="p-20 text-center",
                    ),
                )
            ),
            class_name="mt-8 bg-white rounded-[2rem] border border-slate-200 shadow-sm overflow-hidden",
        ),
        class_name="animate-in fade-in duration-500 space-y-6",
    )