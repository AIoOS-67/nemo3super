"""Terminal multi-turn chat with Nemotron. Run: python chat.py"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ["NVIDIA_API_KEY"],
)

history = [{"role": "system", "content": "You are a concise, direct assistant. Reply in the user's language."}]

print("Nemotron 3 Super chat (commands: /reset to clear history, /exit to quit)\n")

while True:
    try:
        user = input("you > ").strip()
    except (EOFError, KeyboardInterrupt):
        break
    if not user:
        continue
    if user == "/exit":
        break
    if user == "/reset":
        history = history[:1]
        print("(history cleared)\n")
        continue

    history.append({"role": "user", "content": user})
    print("bot > ", end="", flush=True)
    stream = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b",
        messages=history,
        temperature=0.4,
        max_tokens=4096,
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
        stream=True,
    )
    acc = ""
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            piece = chunk.choices[0].delta.content
            acc += piece
            print(piece, end="", flush=True)
    print("\n")
    history.append({"role": "assistant", "content": acc})
