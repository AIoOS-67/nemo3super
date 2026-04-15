import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.environ["NVIDIA_API_KEY"],
)

prompt = "用三句话解释 USDT 稳定币结算对比 Stripe 信用卡结算的核心优势。"

completion = client.chat.completions.create(
    model="nvidia/nemotron-3-super-120b-a12b",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.6,
    top_p=0.95,
    max_tokens=4096,
    extra_body={
        "chat_template_kwargs": {"enable_thinking": True},
        "reasoning_budget": 4096,
    },
    stream=True,
)

print(f"\n【问题】{prompt}\n")
print("【Nemotron 回答】")
in_reasoning = False
for chunk in completion:
    if not chunk.choices:
        continue
    delta = chunk.choices[0].delta
    reasoning = getattr(delta, "reasoning_content", None)
    if reasoning:
        if not in_reasoning:
            print("\n--- 思考过程 ---")
            in_reasoning = True
        print(reasoning, end="", flush=True)
    if delta.content:
        if in_reasoning:
            print("\n\n--- 最终回答 ---")
            in_reasoning = False
        print(delta.content, end="", flush=True)
print("\n")
