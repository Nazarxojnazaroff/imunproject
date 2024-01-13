# Используем базовый образ Python
FROM python:3.9

# Установка рабочей директории в контейнере
WORKDIR /imnpharma

# Копирование всех файлов из корневой папки в контейнер
COPY . /imunpharma

# Обновление интерпретатора и установка зависимостей
RUN pip install --upgrade pip
RUN pip install flask psycopg2-binary

# Запуск команды для запуска приложения
CMD python app.py