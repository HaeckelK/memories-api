from datetime import datetime
import os
from typing import Dict, Tuple, Union, Any

from flask import Flask, request


def create_app(run_as_test: bool=False) -> Flask:
    app = Flask(__name__)
    if run_as_test is False:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URI"]
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    from app.model import db, Memory

    db.init_app(app)

    if run_as_test:
        with app.app_context():
            db.create_all()

    # TODO create dataclass and replace Any
    def serialize_memory(memory: Memory) -> Dict[str, Any]:
        return {
            "id": memory.id,
            "content": memory.content,
            "date_added": memory.date_added,
            "tags": [],
            "next_id": -1,
            "previous_id": -1,
            "concurrent_ids": [],
        }

    @app.route("/")
    def index() -> str:
        return "Memories API"

    @app.route("/memories", methods=["GET"])
    def get_memories() -> Dict[str, Dict[str, str]]:
        memories = Memory.query.all()
        return {x.id: serialize_memory(x) for x in memories}

    @app.route("/memories/<int:id>", methods=["GET"])
    def get_memory(id: int) -> Union[Dict[str, str], Tuple[str, int]]:
        memories = Memory.query.all()
        data = {x.id: serialize_memory(x) for x in memories}
        try:
            return data[id]
        except KeyError:
            return f"Record not found for id {id}", 400

    @app.route("/memories", methods=["POST"])
    def post_memory() -> Dict[str, str]:
        content = request.form.get("content")

        memory = Memory(content=content, date_added=int(today()))
        db.session.add(memory)
        db.session.commit()
        id = memory.id

        memories = Memory.query.all()
        data = {x.id: serialize_memory(x) for x in memories}
        return data[id]

    @app.cli.command("create-db")
    def create_db() -> None:
        print("Creating database")
        db.create_all()
        return

    return app


def today(date_format: str = "%Y%m%d") -> str:
    return datetime.today().strftime(date_format)
