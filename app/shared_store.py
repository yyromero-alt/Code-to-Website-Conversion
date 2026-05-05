import reflex as rx
from sqlalchemy import text


class SharedStore:
    _initialized = False

    @classmethod
    def initialize(cls):
        if cls._initialized:
            return
        cls._initialized = True
        with rx.session() as session:
            session.execute(
                text(
                    "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password_hash TEXT, role TEXT, created_at TEXT)"
                )
            )
            session.execute(
                text(
                    "CREATE TABLE IF NOT EXISTS documents (doc_id TEXT PRIMARY KEY, name TEXT, category TEXT, date TEXT, size TEXT, path TEXT)"
                )
            )
            session.execute(
                text(
                    "CREATE TABLE IF NOT EXISTS shipments (ship_id TEXT PRIMARY KEY, origin TEXT, destination TEXT, status TEXT, progress INTEGER, eta TEXT, items INTEGER, priority TEXT, destinatario TEXT, direccion TEXT, valoracion TEXT, guia TEXT, mes TEXT, docs_obs TEXT, observaciones TEXT)"
                )
            )
            session.execute(
                text(
                    "CREATE TABLE IF NOT EXISTS custom_categories (name TEXT PRIMARY KEY)"
                )
            )
            session.execute(
                text(
                    "CREATE TABLE IF NOT EXISTS inventory_items (item_id TEXT PRIMARY KEY, product_code TEXT, stock_latin INTEGER, stock_imc INTEGER, diferencia INTEGER, estado TEXT, observacion TEXT, imported_at TEXT)"
                )
            )
            session.execute(
                text(
                    "CREATE TABLE IF NOT EXISTS inventory_audits (audit_id TEXT PRIMARY KEY, date TEXT, total_items INTEGER, matched INTEGER, discrepancies INTEGER, accuracy REAL, created_by TEXT)"
                )
            )
            session.execute(
                text(
                    "CREATE TABLE IF NOT EXISTS imc_raw_data (row_id TEXT PRIMARY KEY, referencia TEXT, material TEXT, lote TEXT, stock INTEGER, ubicacion TEXT)"
                )
            )
            session.execute(
                text(
                    "CREATE TABLE IF NOT EXISTS latin_raw_data (row_id TEXT PRIMARY KEY, product_code TEXT, description TEXT, total_stock INTEGER, available_qty INTEGER)"
                )
            )
            docs = session.execute(text("SELECT * FROM documents")).fetchall()
            if not docs:
                session.execute(
                    text(
                        "INSERT INTO documents (doc_id, name, category, date, size, path) VALUES (:doc_id, :name, :category, :date, :size, :path)"
                    ),
                    {
                        "doc_id": "1",
                        "name": "Contrato_2024.pdf",
                        "category": "Contratos",
                        "date": "2024-01-15",
                        "size": "2.4 MB",
                        "path": "",
                    },
                )
                session.execute(
                    text(
                        "INSERT INTO documents (doc_id, name, category, date, size, path) VALUES (:doc_id, :name, :category, :date, :size, :path)"
                    ),
                    {
                        "doc_id": "2",
                        "name": "Factura_001.pdf",
                        "category": "Facturas",
                        "date": "2024-01-14",
                        "size": "156 KB",
                        "path": "",
                    },
                )
                session.execute(
                    text(
                        "INSERT INTO documents (doc_id, name, category, date, size, path) VALUES (:doc_id, :name, :category, :date, :size, :path)"
                    ),
                    {
                        "doc_id": "3",
                        "name": "Manual_Usuario.pdf",
                        "category": "Manuales",
                        "date": "2024-01-12",
                        "size": "5.8 MB",
                        "path": "",
                    },
                )
            ships = session.execute(text("SELECT * FROM shipments")).fetchall()
            if not ships:
                session.execute(
                    text(
                        "INSERT INTO shipments (ship_id, origin, destination, status, progress, eta, items, priority, destinatario, direccion, valoracion, guia, mes, docs_obs, observaciones) VALUES (:ship_id, :origin, :destination, :status, :progress, :eta, :items, :priority, :destinatario, :direccion, :valoracion, :guia, :mes, :docs_obs, :observaciones)"
                    ),
                    {
                        "ship_id": "TRK-9021",
                        "origin": "Almacén Central, Madrid",
                        "destination": "Sucursal Norte, Barcelona",
                        "status": "En camino",
                        "progress": 65,
                        "eta": "18 Feb, 2024",
                        "items": 12,
                        "priority": "Alta",
                        "destinatario": "Cliente Empresa A",
                        "direccion": "Sucursal Norte, Barcelona",
                        "valoracion": "150000",
                        "guia": "9021",
                        "mes": "2",
                        "docs_obs": "REF-1",
                        "observaciones": "",
                    },
                )
            session.commit()

    @classmethod
    def get_users(cls) -> list[dict]:
        cls.initialize()
        with rx.session() as session:
            res = session.execute(text("SELECT * FROM users")).fetchall()
            return [
                {
                    "username": r[0],
                    "password_hash": r[1],
                    "role": r[2],
                    "created_at": r[3],
                }
                for r in res
            ]

    @classmethod
    def add_user(cls, user: dict):
        cls.initialize()
        with rx.session() as session:
            session.execute(
                text(
                    "INSERT INTO users (username, password_hash, role, created_at) VALUES (:username, :password_hash, :role, :created_at)"
                ),
                {
                    "username": user["username"],
                    "password_hash": user["password_hash"],
                    "role": user["role"],
                    "created_at": user["created_at"],
                },
            )
            session.commit()

    @classmethod
    def remove_user(cls, username: str):
        cls.initialize()
        with rx.session() as session:
            session.execute(
                text("DELETE FROM users WHERE username = :username"),
                {"username": username},
            )
            session.commit()

    @classmethod
    def find_user(cls, username: str) -> dict | None:
        cls.initialize()
        with rx.session() as session:
            r = session.execute(
                text("SELECT * FROM users WHERE username = :username"),
                {"username": username},
            ).fetchone()
            return (
                {
                    "username": r[0],
                    "password_hash": r[1],
                    "role": r[2],
                    "created_at": r[3],
                }
                if r
                else None
            )

    @classmethod
    def get_documents(cls) -> list[dict]:
        cls.initialize()
        with rx.session() as session:
            res = session.execute(text("SELECT * FROM documents")).fetchall()
            return [
                {
                    "id": r[0],
                    "doc_id": r[0],
                    "name": r[1],
                    "category": r[2],
                    "date": r[3],
                    "size": r[4],
                    "path": r[5],
                }
                for r in res
            ]

    @classmethod
    def add_document(cls, doc: dict):
        cls.initialize()
        with rx.session() as session:
            d_id = doc.get("id", doc.get("doc_id"))
            session.execute(
                text(
                    "INSERT INTO documents (doc_id, name, category, date, size, path) VALUES (:doc_id, :name, :category, :date, :size, :path)"
                ),
                {
                    "doc_id": d_id,
                    "name": doc["name"],
                    "category": doc["category"],
                    "date": doc["date"],
                    "size": doc["size"],
                    "path": doc.get("path", ""),
                },
            )
            session.commit()

    @classmethod
    def remove_document(cls, doc_id: str):
        cls.initialize()
        with rx.session() as session:
            session.execute(
                text("DELETE FROM documents WHERE doc_id = :doc_id"),
                {"doc_id": doc_id},
            )
            session.commit()

    @classmethod
    def update_document(cls, doc_id: str, updates: dict):
        cls.initialize()
        with rx.session() as session:
            for k, v in updates.items():
                if k == "id":
                    k = "doc_id"
                session.execute(
                    text(
                        f"UPDATE documents SET {k} = :val WHERE doc_id = :doc_id"
                    ),
                    {"val": v, "doc_id": doc_id},
                )
            session.commit()

    @classmethod
    def get_shipments(cls) -> list[dict]:
        cls.initialize()
        with rx.session() as session:
            res = session.execute(text("SELECT * FROM shipments")).fetchall()
            keys = [
                "ship_id",
                "origin",
                "destination",
                "status",
                "progress",
                "eta",
                "items",
                "priority",
                "destinatario",
                "direccion",
                "valoracion",
                "guia",
                "mes",
                "docs_obs",
                "observaciones",
            ]
            out = []
            for r in res:
                d = dict(zip(keys, r))
                d["id"] = d["ship_id"]
                out.append(d)
            return out

    @classmethod
    def set_shipments(cls, shipments: list[dict]):
        cls.initialize()
        with rx.session() as session:
            session.execute(text("DELETE FROM shipments"))
            for s in shipments:
                s_copy = s.copy()
                s_id = s_copy.get("id", s_copy.get("ship_id"))
                params = {
                    "ship_id": s_id,
                    "origin": s_copy["origin"],
                    "destination": s_copy["destination"],
                    "status": s_copy["status"],
                    "progress": s_copy["progress"],
                    "eta": s_copy["eta"],
                    "items": s_copy["items"],
                    "priority": s_copy["priority"],
                    "destinatario": s_copy["destinatario"],
                    "direccion": s_copy["direccion"],
                    "valoracion": s_copy["valoracion"],
                    "guia": s_copy["guia"],
                    "mes": s_copy["mes"],
                    "docs_obs": s_copy["docs_obs"],
                    "observaciones": s_copy["observaciones"],
                }
                session.execute(
                    text(
                        "INSERT INTO shipments (ship_id, origin, destination, status, progress, eta, items, priority, destinatario, direccion, valoracion, guia, mes, docs_obs, observaciones) VALUES (:ship_id, :origin, :destination, :status, :progress, :eta, :items, :priority, :destinatario, :direccion, :valoracion, :guia, :mes, :docs_obs, :observaciones)"
                    ),
                    params,
                )
            session.commit()

    @classmethod
    def remove_shipment(cls, ship_id: str):
        cls.initialize()
        with rx.session() as session:
            session.execute(
                text("DELETE FROM shipments WHERE ship_id = :ship_id"),
                {"ship_id": ship_id},
            )
            session.commit()

    @classmethod
    def get_custom_categories(cls) -> list[str]:
        cls.initialize()
        with rx.session() as session:
            res = session.execute(
                text("SELECT name FROM custom_categories")
            ).fetchall()
            return [r[0] for r in res]

    @classmethod
    def add_custom_category(cls, cat: str):
        cls.initialize()
        with rx.session() as session:
            exists = session.execute(
                text("SELECT name FROM custom_categories WHERE name = :name"),
                {"name": cat},
            ).fetchone()
            if not exists:
                session.execute(
                    text("INSERT INTO custom_categories (name) VALUES (:name)"),
                    {"name": cat},
                )
                session.commit()

    @classmethod
    def get_inventory_items(cls) -> list[dict]:
        cls.initialize()
        with rx.session() as session:
            res = session.execute(
                text("SELECT * FROM inventory_items")
            ).fetchall()
            keys = [
                "item_id",
                "product_code",
                "stock_latin",
                "stock_imc",
                "diferencia",
                "estado",
                "observacion",
                "imported_at",
            ]
            return [dict(zip(keys, r)) for r in res]

    @classmethod
    def set_inventory_items(cls, items: list[dict]):
        cls.initialize()
        with rx.session() as session:
            session.execute(text("DELETE FROM inventory_items"))
            for item in items:
                session.execute(
                    text(
                        "INSERT INTO inventory_items (item_id, product_code, stock_latin, stock_imc, diferencia, estado, observacion, imported_at) VALUES (:item_id, :product_code, :stock_latin, :stock_imc, :diferencia, :estado, :observacion, :imported_at)"
                    ),
                    item,
                )
            session.commit()

    @classmethod
    def remove_inventory_item(cls, item_id: str):
        cls.initialize()
        with rx.session() as session:
            session.execute(
                text("DELETE FROM inventory_items WHERE item_id = :item_id"),
                {"item_id": item_id},
            )
            session.commit()

    @classmethod
    def get_inventory_audits(cls) -> list[dict]:
        cls.initialize()
        with rx.session() as session:
            res = session.execute(
                text("SELECT * FROM inventory_audits")
            ).fetchall()
            keys = [
                "audit_id",
                "date",
                "status",
                "total_items",
                "matched",
                "discrepancies",
                "accuracy",
                "created_by",
                "notes",
            ]
            return [dict(zip(keys, r)) for r in res]

    @classmethod
    def add_inventory_audit(cls, audit: dict):
        cls.initialize()
        with rx.session() as session:
            session.execute(
                text(
                    "INSERT INTO inventory_audits (audit_id, date, status, total_items, matched, discrepancies, accuracy, created_by, notes) VALUES (:audit_id, :date, :status, :total_items, :matched, :discrepancies, :accuracy, :created_by, :notes)"
                ),
                audit,
            )
            session.commit()

    @classmethod
    def remove_inventory_audit(cls, audit_id: str):
        cls.initialize()
        with rx.session() as session:
            session.execute(
                text("DELETE FROM inventory_audits WHERE audit_id = :audit_id"),
                {"audit_id": audit_id},
            )
            session.commit()

    @classmethod
    def get_imc_raw_data(cls) -> list[dict]:
        cls.initialize()
        with rx.session() as session:
            res = session.execute(text("SELECT * FROM imc_raw_data")).fetchall()
            keys = [
                "row_id",
                "referencia",
                "material",
                "lote",
                "stock",
                "ubicacion",
            ]
            return [dict(zip(keys, r)) for r in res]

    @classmethod
    def set_imc_raw_data(cls, items: list[dict]):
        cls.initialize()
        with rx.session() as session:
            session.execute(text("DELETE FROM imc_raw_data"))
            for item in items:
                session.execute(
                    text(
                        "INSERT INTO imc_raw_data (row_id, referencia, material, lote, stock, ubicacion) VALUES (:row_id, :referencia, :material, :lote, :stock, :ubicacion)"
                    ),
                    item,
                )
            session.commit()

    @classmethod
    def get_latin_raw_data(cls) -> list[dict]:
        cls.initialize()
        with rx.session() as session:
            res = session.execute(
                text("SELECT * FROM latin_raw_data")
            ).fetchall()
            keys = [
                "row_id",
                "product_code",
                "description",
                "total_stock",
                "available_qty",
            ]
            return [dict(zip(keys, r)) for r in res]

    @classmethod
    def load_all_data(cls) -> dict:
        """Load documents, shipments, and custom categories in a single session."""
        cls.initialize()
        with rx.session() as session:
            docs_res = session.execute(
                text("SELECT * FROM documents")
            ).fetchall()
            ships_res = session.execute(
                text("SELECT * FROM shipments")
            ).fetchall()
            cats_res = session.execute(
                text("SELECT name FROM custom_categories")
            ).fetchall()
        docs = [
            {
                "id": r[0],
                "doc_id": r[0],
                "name": r[1],
                "category": r[2],
                "date": r[3],
                "size": r[4],
                "path": r[5],
            }
            for r in docs_res
        ]
        ship_keys = [
            "ship_id",
            "origin",
            "destination",
            "status",
            "progress",
            "eta",
            "items",
            "priority",
            "destinatario",
            "direccion",
            "valoracion",
            "guia",
            "mes",
            "docs_obs",
            "observaciones",
        ]
        shipments = []
        for r in ships_res:
            d = dict(zip(ship_keys, r))
            d["id"] = d["ship_id"]
            shipments.append(d)
        custom_categories = [r[0] for r in cats_res]
        return {
            "documents": docs,
            "shipments": shipments,
            "custom_categories": custom_categories,
        }

    @classmethod
    def load_all_inventory_data(cls) -> dict:
        """Load all inventory-related tables in a single session."""
        cls.initialize()
        with rx.session() as session:
            inv_res = session.execute(
                text("SELECT * FROM inventory_items")
            ).fetchall()
            audit_res = session.execute(
                text("SELECT * FROM inventory_audits")
            ).fetchall()
            imc_res = session.execute(
                text("SELECT * FROM imc_raw_data")
            ).fetchall()
            latin_res = session.execute(
                text("SELECT * FROM latin_raw_data")
            ).fetchall()
        inv_keys = [
            "item_id",
            "product_code",
            "stock_latin",
            "stock_imc",
            "diferencia",
            "estado",
            "observacion",
            "imported_at",
        ]
        inventory_items = [dict(zip(inv_keys, r)) for r in inv_res]
        audit_keys = [
            "audit_id",
            "date",
            "status",
            "total_items",
            "matched",
            "discrepancies",
            "accuracy",
            "created_by",
            "notes",
        ]
        inventory_audits = [dict(zip(audit_keys, r)) for r in audit_res]
        imc_keys = [
            "row_id",
            "referencia",
            "material",
            "lote",
            "stock",
            "ubicacion",
        ]
        imc_raw_data = [dict(zip(imc_keys, r)) for r in imc_res]
        latin_keys = [
            "row_id",
            "product_code",
            "description",
            "total_stock",
            "available_qty",
        ]
        latin_raw_data = [dict(zip(latin_keys, r)) for r in latin_res]
        return {
            "inventory_items": inventory_items,
            "inventory_audits": inventory_audits,
            "imc_raw_data": imc_raw_data,
            "latin_raw_data": latin_raw_data,
        }

    @classmethod
    def set_latin_raw_data(cls, items: list[dict]):
        cls.initialize()
        with rx.session() as session:
            session.execute(text("DELETE FROM latin_raw_data"))
            for item in items:
                session.execute(
                    text(
                        "INSERT INTO latin_raw_data (row_id, product_code, description, total_stock, available_qty) VALUES (:row_id, :product_code, :description, :total_stock, :available_qty)"
                    ),
                    item,
                )
            session.commit()