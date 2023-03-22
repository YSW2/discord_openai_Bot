import openai
import os

openai.api_key = os.environ.get('openai_API_KEY')
messages = [{"role": "system",
             "content": "you have to answer user's questions."+
                        "Your name is 멍청이."+
                        "Use a angry tone of speaking when you answer."}]

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