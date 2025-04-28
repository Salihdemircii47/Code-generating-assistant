# Python tabanlı küçük boyutlu bir image
FROM python:3.10-slim-bookworm

# Çevre değişkenlerini ayarlıyoruz
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=Europe/Istanbul

# Sistem bağımlılıklarını kur
RUN apt-get update && apt-get install -y build-essential

# Çalışma dizini oluştur
WORKDIR /app

# Tüm dosyaları container'a kopyala
COPY . /app

# pip güncelle ve bağımlılıkları yükle
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Flask uygulamasının çalışacağı port
EXPOSE 5000

# Uygulamayı başlat
CMD ["python", "app.py"]
