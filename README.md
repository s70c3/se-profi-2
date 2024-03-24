# se-profi-2

# Запуск приложения
Для сбора приложения выполните следующие команды:

```docker-compose build```

```docker-compose up```

Приложение запущено на http://127.0.0:9024
Доступ к документации API (формат Swagger) после запуска контейнера может быть осуществлен по адресу: http://127.0.0.1:9024/docs.

#Описание реализованного приложения:
Приложение реализовано на языке программирования Python. Для реализации приложения выбраны СУБД PostgreSQL для записи логов как бесплатная и открытая. В качестве провайдера доступа используется фреймворк SQLAlchemy. Для реализации API выбран фреймворк FastAPI, позволяющий автоматически создавать документацию в формате Swagger.
