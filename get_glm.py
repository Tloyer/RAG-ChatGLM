import json
from openai import OpenAI
from zhipuai import ZhipuAI
from tqdm import tqdm

def get_glm_response(prompt):
    client = ZhipuAI(api_key="") # 这里填key
    try:
        stream = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="glm-4-public",
            temperature=0.95,
            top_p=0.7,
            stream=True,
            max_tokens=1024
        )
        response = ''
        for part in stream:
            response += part.choices[0].delta.content
        return response
    except Exception as e:
        print(e)
        return None

if __name__ == '__main__':
    response = get_glm_response(prompt="hello")
    print(response)
