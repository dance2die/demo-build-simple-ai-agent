def add(a: int, b: int) -> int:
    return a + b


def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"


NOTES = []
def save_note(note: str) -> str:
    """save a note"""
    NOTES.append(note)
    return f"Saved the note: {note}"


def search_notes(query: str = "*") -> str:
    """
    Search notes
    Passing "*" returns all notes
    """
    if query == "*":
        return "\n".join(NOTES)

    matches = [
        note for note in NOTES
        if query.casefold() in note.casefold()
    ]

    if not matches:
        return "No matching notes found"
    return "\n".join(matches)




ALLOWED_TOOLS = {
    "add": add,
    "get_weather": get_weather,
    "save_note": save_note,
    "search_notes": search_notes,
}
MAX_MODEL_TURNS = 10
TOOLS = [{
    "type": "function",
    "function": {
        "name": "add",
        "description": "Add two whole numbers.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"}
            },
            "required": ["a", "b"],
            "additionalProperties": False
        }
    }
}, {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the weather in a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"],
            "additionalProperties": False
        }
    }
}, {
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
        "description": "Search notes",
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

