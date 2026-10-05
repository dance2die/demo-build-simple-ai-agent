from typing import List
import sqlite3

DB_PATH = "notes.db"

def init_db():
    """
    Initialize the database and create the table if missing
    """
    with  sqlite3.connect(DB_PATH) as connection:
        # make rows accessible like dicts
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        """)
        connection.commit()
    return connection

init_db()

def save_note(note: str) -> str:
    """save a note"""
    note = note.strip()
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT 1 FROM notes WHERE content = ? COLLATE NOCASE LIMIT 1",
            (note,),
        )
        if cursor.fetchone():
            return f"Already saved: {note}"

        cursor.execute(
            "INSERT INTO notes (content) VALUES (?)",
            (note,),
        )
    return f"Saved the note: {note}"


def clear_notes() -> str:
    """delete all notes"""
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("DELETE FROM notes")
        connection.commit()
    return "Cleared all notes"


def delete_note(ids: List[int]) -> str:
    """delete notes based on their id."""
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        placeholders = ", ".join(["?" for _ in ids])
        cursor.execute(f"DELETE FROM notes WHERE id IN ({placeholders})", ids)
        connection.commit()
    return f"Deleted the note(s) with id: {ids}"


def search_notes(query: str = "*") -> str:
    """
    Search notes
    Passing "*" returns all notes
    """
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT id, content FROM notes")
        notes = cursor.fetchall()

    note_texts = [f"{row['id']}: {row['content']}" for row in notes]
    if query == "*":
        return "\n".join(note_texts)

    matches = [
        note for note in note_texts
        if query.casefold() in note.casefold()
    ]

    if not matches:
        return "No matching notes found"
    return "\n".join(matches)


TOOLS = [{
    "type": "function",
    "function": {
        "name": "save_note",
        "description": "Save a note",
        "parameters": {
            "type": "object",
            "properties": {
                "note": {"type": "string"}
            },
            "required": ["note"],
            "additionalProperties": False
        }
    }
}, {
    "type": "function",
    "function": {
        "name": "search_notes",
        "description": "Search notes. Searching '*' means 'all notes'.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
}, {
    "type": "function",
    "function": {
        "name": "delete_note",
        "description": "Delete notes based on their id.",
        "parameters": {
            "type": "object",
            "properties": {
                "ids": {
                    "type": "array",
                    "items": {"type": "integer"}
                }
            },
            "required": ["ids"],
            "additionalProperties": False
        }
    }
}, {
    "type": "function",
    "function": {
        "name": "clear_notes",
        "description": "Delete all notes.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    }
}]