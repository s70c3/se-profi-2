# se-profi-2

# Запуск приложения
Для сбора приложения выполните следующие команды:

```docker-compose build```

```docker-compose up```

Приложение запущено на http://127.0.0:9024
Доступ к документации API (формат Swagger) после запуска контейнера может быть осуществлен по адресу: http://127.0.0.1:9024/docs.

Доступные эндпоинты:

POST: /create_vm/ - добавление виртуальной машины

GET: /servers_utilization/ - получение утилизации всех серверов

GET: /server_utilization/{server_id} - получение утилизации конкретного сервера

# Описание реализованного приложения:
Приложение реализовано на языке программирования Python. Для реализации приложения выбраны СУБД PostgreSQL для записи логов как бесплатная и открытая. В качестве провайдера доступа используется фреймворк SQLAlchemy. Для реализации API выбран фреймворк FastAPI, позволяющий автоматически создавать документацию в формате Swagger.

Приложение позволяет отправить запрос на создание виртуальной машины (и в том числе в теле возможна передача файла, но пока на сервере не осуществляется обработка), а также просмотреть утилизацию кластеров и конкретного сервера.
