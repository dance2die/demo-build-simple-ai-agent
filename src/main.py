import functools
import inspect
import json
import asyncio
import httpx
from tools import (
    save_note, search_notes, add, get_weather,
    TOOLS, ALLOWED_TOOLS, MAX_MODEL_TURNS
)


URL = "http://172.22.0.1:1234/v1/chat/completions"
# URL = "http://127.0.0.1:54504/v1/chat/completions"
MODEL = "google/gemma-4-12b"
payload = {
    "model": MODEL,
    "messages": [{"role": "system", "content": "be consice"}],
    "stream": False
}

async def ask_model(client, messages):
    response = await client.post(URL, json = {
        "model": MODEL,
        "messages": messages,
        "tools": TOOLS,
        "stream": False
    })
    response.raise_for_status()
    return response.json()["choices"][0]["message"]


def run_tool(tool_call):
    name = tool_call["function"]["name"]
    function = ALLOWED_TOOLS.get(name)

    if function is None:
        raise ValueError(f"Unknown tool: {name}")
    
    args = json.loads(tool_call["function"]["arguments"])

    if not isinstance(args, dict):
        raise ValueError(f"Args must be a dict, got {type(args)}")

    print("Requested tool:", function.__name__, args)
    # Check that function accepts these arg names
    inspect.signature(function).bind(**args)

    return function(**args)


async def handle_user_messages(client, messages):
    for turn in range(MAX_MODEL_TURNS):
        response = await ask_model(client, messages)
        tool_calls = response.get("tool_calls") or []

        # No tool calls: this is the final answer
        if not tool_calls:
            answer = response.get("content") or ""
            messages.append({"role": "assistant", "content": answer})
            return answer

        # Don't start new tools on the last allowed model turn
        if turn == MAX_MODEL_TURNS - 1:
            answer = "Stopped: reached the model-turn limit"
            messages.append({"role": "assistant", "content": answer})
            return answer

        # Save the model's request, then run each requested tool.
        tool_request = {"role": "assistant", "tool_calls": tool_calls}
        if response.get("content") is not None:
            tool_request["content"] = response.get("content")
        messages.append(tool_request)

        for call in tool_calls:
            try:
                result = run_tool(call)
            except (ValueError, TypeError, KeyError) as error:
                result = f"Tool error: {error}"

            messages.append({
                "role": "tool", 
                "tool_call_id": call["id"], 
                "content": str(result)
            })

    return "Stopped: reached the model-turn limit."


async def main():
    messages = [{
        "role": "system", 
        "content": """Be concise.
Use add for addition and get_weather for weather questions.
Do not invent weather results.
When asked to remember something, call save_note before confirming.
When asked about personal details, call search_notes before answering. 
for example "what is my name", "what is my favorite color", "what is my favorite food", etc.
When asked to recall or list saved notes, call search_notes before answering.
Use query="*" to list all notes.
Never claim notes were saved or found unless the tool result confirms it.
"""
    }]
    async with httpx.AsyncClient(timeout=120) as client:
        while True:
            user_prompt = input("Prompt (or quit)/> ")
            if user_prompt.lower() in ["quit", "exit", "q", "e"]:
                break

            messages.append({"role": "user", "content": user_prompt})
            answer = await handle_user_messages(client, messages)
            print(f"Agent: {answer}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError, EOFError):
        print("\n\nSession ended via Ctrl+C. Goodbye!")
