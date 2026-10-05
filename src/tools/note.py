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
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO notes (content)
            VALUES (?)
        """, (note,))
        connection.commit()
    return f"Saved the note: {note}"


def search_notes(query: str = "*") -> str:
    """
    Search notes
    Passing "*" returns all notes
    """
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT content FROM notes")
        notes = cursor.fetchall()

    note_texts = [row["content"] for row in notes]
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
}]