from typing import TypedDict


class UserData(TypedDict):
    username: str
    password_hash: str
    role: str
    created_at: str


class DocumentData(TypedDict):
    doc_id: str
    name: str
    category: str
    date: str
    size: str
    path: str


class ShipmentData(TypedDict):
    ship_id: str
    origin: str
    destination: str
    status: str
    progress: int
    eta: str
    items: int
    priority: str
    destinatario: str
    direccion: str
    valoracion: str
    guia: str
    mes: str
    docs_obs: str
    observaciones: str


class CustomCategoryData(TypedDict):
    name: str