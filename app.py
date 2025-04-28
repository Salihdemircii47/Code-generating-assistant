from flask import Flask, request, render_template
import requests, re, os, json
from dotenv import load_dotenv

load_dotenv()
print("OLLAMA API URL:", os.getenv("OLLAMA_API_URL"))

app = Flask(__name__)

system_prompt=(
    Sen bir yapay zeka asistanisin. Kulanicinin verdiği görevi aşağidaki 'Job' sinifi yapisina  uygun şekilde Python kodu yazarak çözmelisin.

İşte 'Job' sinifi:

class Job:
    def __init__(self, asset):
        self.asset = asset
        self.output = None
        self.score = None

    def run(self):
        # Buraya kullanıcının isteğine göre işlem yapılacak kod yazılacak
        pass

    def calculate_score(self):
        # Çıktıya göre bir skor hesaplanacak
        pass

Kurallar:
- Ürettiğin tüm kod bu sinigi genişletmeli veya bu sinifa uygun olmali.
- 'run' metodunda asil işi yap.
- 'calculate_score' metodunda işlemin başarimini değerlendir.
- asset, output ve score gibi özellikleri kullan.

Lütfen sadece bu yapiya uygun Python kodu üret.

Çikti formatin şu şekilde olsun:
Başlik: {Başlik buraya}
Kod:
```python
# Kod burada
)
def generate_code(prompt):
    url = "http://localhost:11434/api/chat"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "llama3",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    content = response.json()["message"]["content"]
    return content

    response = requests.post(url, headers=headers, json=data)
    content = response.json()["message"]["content"]
    return content


def parse_response(full_content):
    """
    Model çıktısından başlık ve kodu ayrıştırır.
    """
    match = re.search(r"(?P<title>.*?)\n```python\n(?P<code>.*?)\n```", full_content, re.DOTALL)

    if match:
        title = match.group("title").strip()
        code = match.group("code").strip()
        return title, code
    else:
        return "Başlık/Kod Ayrıştırılamadı", full_content


def ollama_prompt(prompt_text):
    url = "http://localhost:11434/api/chat"
    data = {
        "model": "codellama:7b-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt_text}
        ],
        "stream": False   # BURAYI EKLEDİK! 👈
    }
    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json()["message"]["content"]
    else:
        return "Model yanıt veremedi. Hata kodu: " + str(response.status_code)


    try:
        response = requests.post(url, json=data)
        response.raise_for_status()

        result = response.json()
        content = result["message"]["content"]

        match = re.search(r"(?P<title>.*?)\n```python\n(?P<code>.*?)\n```", content, re.DOTALL)
        if match:
            title = match.group("title").strip()
            code = match.group("code").strip()
            return title, code
        else:
            return "Başlık/Kod ayrıştırılamadı", content
    except Exception as e:
        return "Hata", str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    title = code = None
    if request.method == 'POST':
        prompt = request.form['prompt']
        title, code = ollama_prompt(prompt)
    return render_template('index.html', title=title, code=code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
