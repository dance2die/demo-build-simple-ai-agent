import asyncio
import httpx

async def call_local_llm():
    url = "http://172.22.0.1:1234/v1/chat/completions"
    payload = {
        "model": "google/gemma-4-12b",
        "messages": [{"role": "user", "content": "What is 2+2?"}],
        "stream": False
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            
            data = response.json()
            print(data["choices"][0]["message"]["content"])
            
        except httpx.HTTPError as e:
            print(f"HTTP Error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(call_local_llm())
