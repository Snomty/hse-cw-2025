# Этап 1: Базовый образ с явным тегом (вместо python:3.9-slim-bookworm)
FROM python:3.9.18-slim

WORKDIR /app

# 1. Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 2. Установка Python-зависимостей в правильном порядке
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
    numpy==1.23.5 \
    scipy==1.9.3 \
    scikit-learn==1.1.3 \
    && pip install --no-cache-dir -r requirements.txt

# 3. Проверка версий
RUN python -c "import numpy as np; print(f'NUMPY VERSION: {np.__version__}')"

# 4. Копирование кода
COPY . .

CMD ["python", "telegram-bot/homeprice_bot.py"]