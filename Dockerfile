# Этап 1: Установка системных зависимостей с кешированием
FROM python:3.9-slim as builder

# Кешируем apt-пакеты (обновляем только при изменении этого блока)
RUN echo "Updating apt packages..." && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev && \
    rm -rf /var/lib/apt/lists/*

# Этап 2: Основной образ
FROM python:3.9-slim
WORKDIR /app

# Копируем системные зависимости из builder
COPY --from=builder /usr/lib /usr/lib
COPY --from=builder /usr/include /usr/include

# Устанавливаем Python-зависимости (кешируются отдельно)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

CMD ["python", "telegram-bot/homeprice_bot.py"]