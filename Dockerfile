FROM python:3.9.18-slim

WORKDIR /app

# 1. Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 2. Установка Python-зависимостей в правильном порядке
COPY requirements.txt .
RUN pip install --upgrade "pip<23.1" && \
    pip install --no-cache-dir \
    numpy==1.22.4 \
    scipy==1.8.1 \
    scikit-learn==1.1.2 \
    && pip install --no-cache-dir -r requirements.txt

# 3. Проверка версий
RUN python -c "import numpy; print(f'NUMPY: {numpy.__version__}'); \
              import sklearn; print(f'SKLEARN: {sklearn.__version__}')"

# 4. Копирование кода
COPY . .

CMD ["python", "telegram-bot/homeprice_bot.py"]