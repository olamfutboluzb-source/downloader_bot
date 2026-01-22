FROM python:3.10-slim

# Установка ffmpeg и системных библиотек
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    python3-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё (включая cookies.txt)
COPY . .

# Создаем папку для загрузок в /tmp (там всегда есть права)
RUN mkdir -p /tmp/downloads && chmod 777 /tmp/downloads

EXPOSE 7860

CMD ["python", "main.py"]
