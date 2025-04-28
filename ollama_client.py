import requests
import re
import os
import json


def ollama_prompt(prompt_text):
    url = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/chat")  # .env'den oku
    
    data = {
        "model": "codellama:7b-instruct",
        "messages": [
            {"role": "system", "content": "Write a short title and then a valid Python code. Respond in this format:\nTitle\n```python\n# code here\n```"},
            {"role": "user", "content": prompt_text}
        ]
    }

    try:
        response = requests.post(url, json=data, stream=True)

        full_content = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                data = json.loads(decoded_line)
                if "message" in data and "content" in data["message"]:
                    full_content += data["message"]["content"]

        print("🔧 Model Birleşik Cevap:\n", full_content)

        match = re.search(r"(?P<title>.*?)\n```python\n(?P<code>.*?)\n```", full_content, re.DOTALL)
        if match:
            title = match.group("title").strip()
            code = match.group("code").strip()
            return title, code
        else:
            return "Başlık/Kod ayrıştırılamadı", full_content
        

    except Exception as e:
        return "Hata", str(e)

