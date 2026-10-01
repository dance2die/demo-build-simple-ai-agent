import asyncio
import httpx

url = "http://172.22.0.1:1234/v1/chat/completions"
payload = {
    "model": "google/gemma-4-12b",
    "messages": [{"role": "system", "content": "be consice"}],
    "stream": False
}

async def call_local_llm(user_prompt: str = "What is 2+2?"):
    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0, connect=10.0)) as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            
            data = response.json()
            message = data["choices"][0]["message"]["content"]
            # print(f"The answer is : {message}")
            return message
            
        except httpx.HTTPError as e:
            print(f"HTTP Error occurred: {e}")


async def main():
    user_prompt = input("What color do you like????: ")
    payload["messages"].append({"role": "user", "content": user_prompt})
    reply = await call_local_llm()
    payload["messages"].append({"role": "assistant", "content": reply})
    print(reply)

    user_prompt = input("So what?: ")
    payload["messages"].append({"role": "user", "content": user_prompt})
    reply = await call_local_llm()
    payload["messages"].append({"role": "assistant", "content": reply})
    print(reply)



if __name__ == "__main__":
    asyncio.run(main())
