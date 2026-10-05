from tools.note import save_note, search_notes, TOOLS as DB_TOOLS


def add(a: int, b: int) -> int:
    return a + b


def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"


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
}, *DB_TOOLS]

