import openai
import os

openai.api_key = os.getenv('openai_API_KEY')

class openai_bot:
    def __init__(self):
        with open("system_content.txt", 'r') as f:
            sys_order = ' '.join(f.readlines())
        self.messages = [{"role": "system", "content": sys_order}]
        self.token_num = 0

    async def usegpt(self, question):
        # 질문과 대답 저장
        self.messages.append({"role": "user", "content": question})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        print(completion)
        answer = completion['choices'][0]['message']['content']
        self.messages.append({"role": "assistant", "content": answer})
        return answer

    async def messages_clear(self):
        with open("system_content.txt", 'r') as f:
            sys_order = ' '.join(f.readlines())
        self.messages = [{"role": "system", "content": sys_order}]
