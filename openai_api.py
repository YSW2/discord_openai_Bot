import openai
import os

openai.api_key = os.getenv('openai_API_KEY')

with open("system_content.txt", 'r') as f:
    sys_order = ''.join(f.readlines())

messages = [{"role": "system",
             "content": sys_order}]

async def usegpt(question):

    print(f"{question}")

    # 질문과 대답 저장

    messages.append({"role": "user", "content": question})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    answer = completion['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": answer})

    return answer